"""
练习 2：MessagesPlaceholder —— 动态插入历史消息
目标：理解 LangChain 如何管理多轮对话历史（Day3 记忆机制的地基）
运行：在项目根目录执行  python day2\\02_message_placeholder.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

# MessagesPlaceholder：运行时把"任意长度的消息列表"塞进这个位置
# 对比 D1 练习4 手动 append 消息，这里历史可以任意长、随时替换
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深健身教练，回答要简短实用。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

# 模拟第一轮对话
history = []
r1 = chain.invoke({"history": history, "question": "我体重80kg，想减肥，怎么开始？"})
print("第1轮:", r1.content)

# 把刚才的对话追加进 history，再问第二轮 —— 模型"记住"了前文
history += [("human", "我体重80kg，想减肥，怎么开始？"), ("ai", r1.content)]
r2 = chain.invoke({"history": history, "question": "那每天应该跑多久？"})
print("第2轮:", r2.content)
