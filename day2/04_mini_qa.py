"""
练习 4：综合小项目 —— 产品知识问答链（Day4 RAG 的雏形）
目标：把 模板 + 知识注入 + 链 组合成"带知识库的问答"，体会"知识边界"约束
运行：在项目根目录执行  python day2\\04_mini_qa.py
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

# 模拟"检索到的知识"（Day4 会用向量库自动检索，这里先手写一段）
knowledge = """
【豆包 Pro】月费 30 元，支持 128K 上下文、联网搜索、图片生成 500 张/月。
【豆包 Lite】免费，支持 32K 上下文，不含联网搜索。
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是产品客服。只能根据提供的知识回答，知识里没有的内容就明确说不知道。\n\n知识库：\n{knowledge}"),
    ("human", "{question}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.2,  # 客服场景要稳定，用低温
)

chain = prompt | llm | StrOutputParser()

for q in ["豆包 Pro 多少钱一个月？", "豆包能生成图片吗？", "豆包怎么修电脑？"]:
    print(f"Q: {q}")
    print(f"A: {chain.invoke({'knowledge': knowledge, 'question': q})}\n")
