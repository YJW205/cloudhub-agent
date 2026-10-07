"""
练习 3：输出解析器 —— 手写 JSON 解析（对比 D1 的 function_calling 方式）
目标：理解结构化输出的第二种实现方式：提示词指令 + 文本解析
运行：在项目根目录执行  python day2\\03_output_parser.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

class Product(BaseModel):
    name: str = Field(description="产品名称")
    price: float = Field(description="价格（元）")
    selling_point: str = Field(description="一句话卖点")

# PydanticOutputParser：把"输出格式说明"注入提示词，再解析模型吐出的 JSON 文本
parser = PydanticOutputParser(pydantic_object=Product)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是电商文案。必须严格按要求的 JSON 格式输出。\n{format_instructions}"),
    ("human", "为一款保温杯写一条产品介绍"),
])
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.2,
)

chain = prompt | llm | parser
product = chain.invoke({})

print("返回对象类型:", type(product).__name__)
print("名称:", product.name)
print("价格:", product.price)
print("卖点:", product.selling_point)
