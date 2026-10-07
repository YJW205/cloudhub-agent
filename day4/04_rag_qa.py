"""
练习 4：完整 RAG 问答链 —— 检索 → 增强 → 生成
目标：把检索到的资料拼进提示词，让模型"基于资料回答"，并对比"没有资料直接问"
运行：在项目根目录执行  python day4\\04_rag_qa.py
"""

import os
from pathlib import Path

os.environ.setdefault("HF_HOME", str(Path(__file__).resolve().parent.parent / "models"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.2,  # 客服问答要稳定
)

# 加载向量库 → 检索器
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=str(Path(__file__).resolve().parent.parent / "chroma_db"),
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG 提示词：把检索到的资料作为"依据"注入
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是公司行政助手。只能根据提供的资料回答，资料里没有的信息要明确说不知道。\n\n资料：\n{context}"),
    ("human", "{question}"),
])
rag_chain = rag_prompt | llm | StrOutputParser()

questions = [
    "年假有几天？",
    "出差住宿报销标准是多少？",
    "公司食堂几点开门？",  # 知识库外的问题
]

for q in questions:
    print(f"Q: {q}")

    # 第一步：检索（RAG 的灵魂，先看模型"读到了什么"）
    docs = retriever.invoke(q)
    context = "\n".join(d.page_content for d in docs)
    print(f"── 检索到的资料片段（共 {len(docs)} 块）──")
    for d in docs:
        print(f"  · {d.page_content[:70]}...")

    # 第二步：增强 + 生成
    answer = rag_chain.invoke({"context": context, "question": q})
    print(f"A: {answer}\n")
