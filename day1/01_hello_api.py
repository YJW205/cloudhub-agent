"""
练习 1：第一次调用大模型 API
目标：跑通"模型调用"这条最基础的链路，理解 invoke 的返回值结构
运行：在项目根目录执行  python day1\\01_hello_api.py
"""

from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 自动加载项目根目录的 .env（无论从哪个目录运行都能找到）
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import os
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先按 README 配置 .env 文件")

# DeepSeek 兼容 OpenAI 接口，直接复用 langchain-openai 的 ChatOpenAI
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

# invoke 是最基本的调用方式，返回 AIMessage 对象
result = llm.invoke("用一句话介绍什么是大语言模型")

print("返回对象类型:", type(result).__name__)
print("回复内容:", result.content)
