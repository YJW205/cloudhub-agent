"""
app.py —— 「云枢 CloudHub」产品文档助手（主程序）

架构（LangGraph 图）：
  START → agent(模型思考) → 有 tool_calls? → tools(执行: 检索知识库 / 计算费用) → 回到 agent
                            → 无 tool_calls? → END(输出回答)
  + SqliteSaver checkpoint：多轮记忆（thread_id 区分会话）

能力：
  1. Agentic RAG：模型自主决定何时检索知识库（对比固定流程 RAG 更智能）
  2. 业务工具：套餐费用计算
  3. 多轮记忆：记住用户上下文
  4. 容错：工具失败回传模型重试

运行（先构建索引，再启动）：
  python day6\\build_index.py
  python day6\\app.py
"""

import config
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import Annotated, TypedDict


# ========== 1. 知识库检索器（RAG 基础） ==========
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=config.CHROMA_DIR,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# ========== 2. 工具 ==========
@tool
def retrieve(query: str) -> str:
    """在云枢产品知识库中检索与 query 相关的资料。
    当用户问题涉及产品功能、套餐价格、API 文档、权限体系、故障排查等文档内容时，必须调用本工具。"""
    docs = retriever.invoke(query)
    if not docs:
        return "知识库中没有检索到相关内容。"
    return "\n\n".join(f"[资料{i+1}] {d.page_content}" for i, d in enumerate(docs))


@tool
def subscription_cost(plan: str, seats: int, months: int, yearly: bool = False) -> str:
    """计算云枢 CloudHub 套餐费用。
    plan 为 free/pro/enterprise；seats 为席位数量；months 为购买月数；
    yearly 为 True 表示按年付费（享 8 折）。"""
    prices = {"free": 0, "pro": 89, "enterprise": 299}
    if plan not in prices:
        return f"无效套餐「{plan}」，可选：free / pro / enterprise"
    unit = prices[plan]
    if unit == 0:
        return "免费版无需付费。"
    total = unit * seats * months
    if yearly:
        total = round(total * 0.8)
        return f"{plan} 版 {seats} 席位按年付费 {months} 个月（8 折），费用 {total} 元"
    return f"{plan} 版 {seats} 席位 {months} 个月，费用 {total} 元"


@tool
def check_api_error(error_code: str) -> str:
    """查询云枢开放 API 错误码的含义与处理方法。
    当用户报告 API 返回某个错误码（400/401/403/404/429/500）时调用。"""
    table = {
        "400": "参数错误：请求体缺少必填字段或格式不正确，请检查参数。",
        "401": "认证失败：API Key 无效或已过期（Key 有效期 1 年），或请求头格式错误，请检查。",
        "403": "权限不足：当前账号无权访问该资源，请检查套餐权限。",
        "404": "资源不存在：请求的资源不存在或已被删除，请检查 ID 是否正确。",
        "429": "请求过快：触发限流（每分钟 60 次），请稍后重试或降低请求频率。",
        "500": "服务器内部错误：云枢服务端异常，请稍后重试或联系支持。",
    }
    code = str(error_code).strip()
    if code not in table:
        return f"错误码 {code} 不在文档中（支持：400/401/403/404/429/500）。"
    return f"错误码 {code}：{table[code]}"


tools = [retrieve, subscription_cost, check_api_error]


# ========== 3. LangGraph 图 ==========
class State(TypedDict):
    messages: Annotated[list, add_messages]


# system 提示：教模型"何时检索、何时算费用、何时直接答"（Agentic RAG 的关键）
SYSTEM_PROMPT = """你是「云枢 CloudHub」产品文档助手。规则：
1. 问题涉及产品功能、套餐价格、API、权限、故障排查 → 必须调用 retrieve 工具检索资料后回答，禁止凭记忆编造。
2. 涉及费用计算（席位×价格×月数、折扣）→ 调用 subscription_cost 工具。
3. 检索到的资料里没有的信息，明确说「文档中未找到相关内容」。
4. 回答简洁，先给结论再补充细节。"""


def agent_node(state: State):
    """模型思考：基于全部消息（含工具结果）决定下一步"""
    return {"messages": [llm.invoke(state["messages"])]}


def should_continue(state: State):
    """条件路由：还有工具要调就继续，否则结束"""
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END


def build_app():
    global llm
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        base_url=config.LLM_BASE_URL,
        api_key=config.DEEPSEEK_API_KEY,
        temperature=0.2,
    ).bind_tools(tools)

    graph = StateGraph(State)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    # 持久化记忆（Day5 学过的 SqliteSaver）
    # 注意：不能用 with 块（块结束会关闭连接），直接持有连接供整个程序使用
    import sqlite3
    conn = sqlite3.connect(config.CHECKPOINT_DB, check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)
    return graph.compile(checkpointer=checkpointer)


def main():
    app = build_app()
    print("=== 云枢 CloudHub 产品文档助手 ===")
    print("试试：专业版多少钱？ / 企业版20个席位按年付多少钱？ / Webhook收不到回调怎么办？ / 输入 exit 退出")
    config_thread = {"configurable": {"thread_id": "user_main"}}

    while True:
        question = input("你: ")
        if question.lower() in ("exit", "quit"):
            break
        result = app.invoke({"messages": [("human", question)]}, config=config_thread)
        print("助手:", result["messages"][-1].content)
        print()


if __name__ == "__main__":
    main()
