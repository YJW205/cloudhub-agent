"""
练习 2：让模型"决定"调用工具 —— Agent 循环的核心机制
目标：bind_tools 把工具交给模型，模型输出 tool_calls，你手动执行并回传结果
运行：在项目根目录执行  python day3\\02_tool_calling.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
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


llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
)

# bind_tools：把工具"绑"到模型上 —— 模型从此知道有这些工具可用
llm_with_tools = llm.bind_tools([multiply, get_weather])

# 问一个需要工具的问题
result = llm_with_tools.invoke("帮我算一下 1234 乘以 56 等于多少？")

print("模型是否要求调用工具:", bool(result.tool_calls))
print("tool_calls 原始结构:", result.tool_calls, "\n")

# 关键：此时模型没有直接给答案，而是"申请"调用工具 —— 执行权在你手里
for call in result.tool_calls:
    tool_name = call["name"]
    args = call["args"]
    print(f"→ 模型申请调用: {tool_name}({args})")
    if tool_name == "multiply":
        print("→ 工具执行结果:", multiply.invoke(args))
