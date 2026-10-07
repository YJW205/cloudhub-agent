"""
练习 3：Checkpointer —— LangGraph 官方的记忆方案
目标：checkpoint 自动保存每一步状态；thread_id 区分会话；SQLite 持久化后重启不丢
      对比 Day3 手写 sqlite：这是官方封装，还自动保存完整状态（含中间步骤）
运行：在项目根目录执行  python day5\\03_memory_checkpoint.py
      （建议连续运行两次：第二次模型还记得第一轮的自我介绍）
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

def chat_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(State)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# SqliteSaver：把每一步状态自动存进 SQLite（Day3 手写版的官方封装）
# 注意：from_conn_string 直接透传 sqlite3.connect，传文件路径即可（不是 sqlite:/// URL）
DB = "E:/ai/doubao project/agent_checkpoints.db"
with SqliteSaver.from_conn_string(DB) as checkpointer:
    app = graph.compile(checkpointer=checkpointer)

    # thread_id 像一个"会话 ID"：同一个 ID 共享记忆，不同 ID 相互隔离
    config = {"configurable": {"thread_id": "user_021"}}

    # 第一轮：自我介绍（如果之前运行过，模型会记得——因为消息在 checkpoint 里）
    # r1 = app.invoke({"messages": [("human", "我叫小明，来自佛山，请记住我的名字和城市")]}, config=config)
    print("第1轮回答:", r1["messages"][-1].content)

    # 第二轮：提问验证记忆
    r2 = app.invoke({"messages": [("human", "我叫什么名字？来自哪里？")]}, config=config)
    print("第2轮回答:", r2["messages"][-1].content)

    print("\n状态已存入 agent_checkpoints.db —— 重新运行本脚本，模型依然记得！")
