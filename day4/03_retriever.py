"""
练习 3：检索 —— 向量相似度查询
目标：理解"检索"的本质：把问题也变成向量，找库里最相似的文本块
运行：在项目根目录执行  python day4\\03_retriever.py
"""

import os
from pathlib import Path

os.environ.setdefault("HF_HOME", str(Path(__file__).resolve().parent.parent / "models"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 加载已有的向量库（不用重新构建）
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=str(Path(__file__).resolve().parent.parent / "chroma_db"),
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # 每次取最相似的 3 块

# 测试检索
for question in [
    "年假有几天？",
    "报销打车费有什么规定？",
    "公司有什么健康福利？",
]:
    print(f"Q: {question}")
    docs = retriever.invoke(question)
    print(f"检索到 {len(docs)} 块，按相似度排序:")
    for i, d in enumerate(docs):
        print(f"  [{i+1}] 相似度来源第{d.metadata.get('chunk')}块: {d.page_content[:60]}...")
    print()
