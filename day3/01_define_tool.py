"""
练习 1：定义工具 —— Agent 的"手脚"
目标：用 @tool 把普通函数变成模型可调用的工具，理解工具的 schema 结构
运行：在项目根目录执行  python day3\\01_define_tool.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# @tool 装饰器：把普通函数变成"模型可调用"的工具
@tool
def multiply(a: int, b: int) -> int:
    """两个整数相乘。"""
    return a * b


@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气（模拟数据）。"""
    return f"{city}今天 25℃，多云"


print("=== 工具1: multiply ===")
print("名称:", multiply.name)
print("描述:", multiply.description)
print("参数:", multiply.args)

print("\n=== 工具2: get_weather ===")
print("名称:", get_weather.name)
print("描述:", get_weather.description)
print("参数:", get_weather.args)

print("\n=== 工具也可以直接调用 ===")
print("multiply(6, 7) =", multiply.invoke({"a": 6, "b": 7}))
print("get_weather(广州) =", get_weather.invoke({"city": "广州"}))
