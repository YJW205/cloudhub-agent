"""
练习 4：把 Day3 的手动 Agent 循环改造成 LangGraph 图（今天的重头戏）
目标：Agent = 一张图：
      agent 节点（模型思考）→ 若申请调工具 → tools 节点（执行）→ 回到 agent
      → 直到模型直接回答 → END
      对比 Day3 的 while 循环：图的每个环节都可观测、可中断、可持久化
运行：在项目根目录执行  python day5\\04_agent_graph.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

@tool
def multiply(a: int, b: int) -> int:
    """两个整数相乘。"""
    return a * b


@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气（模拟数据）。"""
    return f"{city}今天 25℃，多云"


tools = [multiply, get_weather]

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.3,
).bind_tools(tools)

# agent 节点：模型"思考"（可能申请调工具，也可能直接回答）
def agent_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# 条件路由：看模型最后一条消息有没有申请调工具
def should_continue(state: State):
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END


graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))  # ToolNode：官方"工具执行"节点

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")  # 工具执行完，回到 agent 继续思考

app = graph.compile()

# 固定测试问题（不交互，方便观察图流转）
for q in ["帮我算 12 乘以 34", "北京天气怎么样？"]:
    result = app.invoke({"messages": [("human", q)]})
    print(f"Q: {q}")
    print("A:", result["messages"][-1].content)
    print()
