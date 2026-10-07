"""
练习 2：向量化 + 存入向量库 —— RAG 的核心
目标：把文本块转成向量（embedding）存入 Chroma，形成"知识索引"
说明：第一次运行会下载中文 embedding 模型（约 100MB，存到项目 models 目录），之后秒开
运行：在项目根目录执行  python day4\\02_build_index.py
"""

import os
from pathlib import Path

# 让模型下载到项目目录（而不是系统缓存），保持"所有内容都在项目里"
os.environ.setdefault("HF_HOME", str(Path(__file__).resolve().parent.parent / "models"))
# 离线模式：模型已在本地缓存，加载时不再联网检查（国内直连 HF 不稳）
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. 加载文档
text = Path(__file__).resolve().parent / "knowledge" / "employee_manual.txt"
content = text.read_text(encoding="utf-8")

# 2. 分割成块
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_text(content)
print(f"共 {len(chunks)} 个文本块\n")

# 3. 向量化：把每块文本变成一串数字（向量），语义相近的文本向量也相近
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
print("embedding 模型加载完成\n")

# 4. 包成 Document 对象（page_content 是正文，metadata 是附加信息，检索时可追溯来源）
docs = [
    Document(page_content=c, metadata={"source": "employee_manual.txt", "chunk": i})
    for i, c in enumerate(chunks)
]

# 5. 存入 Chroma 向量库（本地持久化到 chroma_db 目录，重复运行会重建）
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=str(Path(__file__).resolve().parent.parent / "chroma_db"),
)
print(f"已存入向量库，共 {vectorstore._collection.count()} 个向量")
print("索引构建完成！下一步运行 03_retriever.py 测试检索")
