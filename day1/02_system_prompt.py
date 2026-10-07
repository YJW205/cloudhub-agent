"""
练习 2：System Prompt 与采样参数
目标：理解 system prompt 如何约束角色；temperature 如何影响输出的随机性
运行：python day2\\..\\day1\\02_system_prompt.py  或 在项目根目录 python day1\\02_system_prompt.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

# ChatPromptTemplate：把 system 与 user 消息模板化，变量用 { } 占位
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位严谨的中文老师，回答必须简洁、准确，禁止使用网络用语。"),
    ("human", "{question}"),
])

# 对比 temperature：0 最稳定（适合事实回答），1.5 更发散（适合创意）
for temp in (0.0, 1.5):
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        api_key=api_key,
        temperature=temp,
    )
    # 管道符 | 是 LangChain 的核心语法：prompt → llm 组成一条链
    chain = prompt | llm
    answer = chain.invoke({"question": "「内卷」是什么意思？"})
    print(f"--- temperature={temp} ---")
    print(answer.content)
    print()
