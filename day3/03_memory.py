"""
练习 3：持久化记忆 —— 关闭程序后依然记得
目标：用 SQLite 把对话历史存进本地数据库，程序重启后记忆还在
说明：LangGraph 官方有更高级的 checkpointer 封装（Day5 会用到），
      今天的练习用标准库 sqlite3 手写存取，理解持久化的底层原理：
      把消息存盘 → 下次启动时加载回内存。
运行：在项目根目录执行  python day3\\03_memory.py   （建议连续运行两次观察效果）
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

DB_PATH = Path(__file__).resolve().parent.parent / "memory.db"
SESSION = "user_01"


def ensure_table():
    """启动时先建表（幂等，已存在则跳过）"""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "session_id TEXT, role TEXT, content TEXT)"
        )
        conn.commit()
    finally:
        conn.close()


def load_history():
    """从 SQLite 读取该会话的全部历史消息，返回消息对象列表"""
    msgs = []
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE session_id=? ORDER BY id",
            (SESSION,),
        ).fetchall()
        for role, content in rows:
            if role == "human":
                msgs.append(HumanMessage(content=content))
            else:
                msgs.append(AIMessage(content=content))
    finally:
        conn.close()
    return msgs


def save_message(role: str, content: str):
    """把一条消息写入 SQLite"""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (SESSION, role, content),
        )
        conn.commit()
    finally:
        conn.close()


# 启动时：确保表存在，并加载历史（上次的对话全部恢复）
ensure_table()
history = load_history()
print(f"已从数据库加载 {len(history)} 条历史消息\n")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是旅行规划助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.3,
)
chain = prompt | llm

# 第一轮
q1 = "我叫小明，喜欢安静的海边，帮我推荐一个国内旅游目的地"
r1 = chain.invoke({"history": history, "question": q1})
save_message("human", q1)
save_message("ai", r1.content)
print("第1轮:", r1.content)

# 第二轮
q2 = "预算 5000，两个人，还是推荐海边，具体一点"
r2 = chain.invoke({"history": history, "question": q2})
save_message("human", q2)
save_message("ai", r2.content)
print("第2轮:", r2.content)

print("\n已写入 memory.db —— 现在重新运行本脚本，将看到历史被加载，模型依然记得这段对话！")
