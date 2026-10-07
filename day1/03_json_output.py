"""
练习 3：结构化输出（JSON）
目标：让模型按你定义的 schema 返回 JSON —— 这是后续"工具调用"的地基
运行：在项目根目录执行  python day1\\03_json_output.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

# 用 Pydantic 定义输出结构：字段名 + 类型 + 说明
class MovieReview(BaseModel):
    title: str = Field(description="电影名称")
    score: float = Field(description="评分（0-100 分）")
    comment: str = Field(description="一句话影评")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.3,
)

# with_structured_output 自动让模型返回符合 schema 的对象
# method="function_calling"：DeepSeek 不支持 OpenAI 的 json_schema 响应格式，
# 改用函数调用方式（这也是 Day3 工具调用的核心机制，提前体验）
structured_llm = llm.with_structured_output(MovieReview, method="function_calling")

prompt = ChatPromptTemplate.from_messages([
    ("human", "请评论电影《流浪地球2》"),
])

chain = prompt | structured_llm
review = chain.invoke({})

print("返回对象类型:", type(review).__name__)
print("片名:", review.title)
print("评分:", review.score)
print("影评:", review.comment)
