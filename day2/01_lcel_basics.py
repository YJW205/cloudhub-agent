"""
练习 1：LCEL 管道链 —— LangChain 的"灵魂"
目标：理解 prompt | llm | parser 的管道组合，对比 invoke / stream / batch 三种调用方式
运行：在项目根目录执行  python day2\\01_lcel_basics.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位{role}。"),
    ("human", "{question}"),
])
parser = StrOutputParser()  # 直接把 AIMessage 里的文本取出来（变字符串）

# LCEL：管道符 | 把 模板 → 模型 → 解析器 串成一条链，整条链就像一个函数
chain = prompt | llm | parser

# 1. invoke：一次性调用（最常用）
print("=== invoke ===")
print(chain.invoke({"role": "耐心的老师", "question": "解释一下什么是递归"}))

# 2. stream：流式输出，逐字吐出（打字机效果，生产环境必备）
print("\n=== stream ===")
for chunk in chain.stream({"role": "耐心的老师", "question": "用一句话解释什么是递归"}):
    print(chunk, end="", flush=True)
print()

# 3. batch：批量调用，一次处理多条
print("\n=== batch ===")
results = chain.batch([
    {"role": "数学老师", "question": "1+1=?"},
    {"role": "数学老师", "question": "2+2=?"},
])
for r in results:
    print("-", r)
