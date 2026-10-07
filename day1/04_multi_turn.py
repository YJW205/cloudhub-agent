"""
练习 4：多轮对话（消息序列）
目标：理解 Chat 模型的消息结构 —— 消息序列就是 Agent "记忆"的地基
运行：在项目根目录执行  python day1\\04_multi_turn.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

# 消息序列：system 设定 + 用户提问
messages = [
    ("system", "你是一个行程规划助手。"),
    ("human", "我明天去北京出差，帮我安排一天的行程。"),
]
reply1 = llm.invoke(messages)
print("第 1 轮回复:", reply1.content, "\n")

# 把上一轮回答追加进序列 → 模型就"记住"了前文
messages.append(("ai", reply1.content))
messages.append(("human", "行程太赶了，去掉下午的安排，重新规划。"))

reply2 = llm.invoke(messages)
print("第 2 轮回复:", reply2.content)
