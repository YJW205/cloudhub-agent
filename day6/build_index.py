"""
build_index.py —— 构建云枢产品知识库索引
把 saas_product_docs.txt 分割、向量化、存入 Chroma（与 Day4 同一向量库）
运行：python day6\\build_index.py
"""

import config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. 加载知识库文档
content = config.KNOWLEDGE_FILE.read_text(encoding="utf-8")
print(f"加载文档: {config.KNOWLEDGE_FILE.name}（{len(content)} 字）")

# 2. 分割（chunk 稍大：产品文档问题往往需要完整段落上下文）
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60)
chunks = splitter.split_text(content)
print(f"分割为 {len(chunks)} 块")

# 3. 向量化
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
print("embedding 模型加载完成")

# 4. 存入向量库
docs = [
    Document(page_content=c, metadata={"source": config.KNOWLEDGE_FILE.name, "chunk": i})
    for i, c in enumerate(chunks)
]
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=config.CHROMA_DIR,
)
print(f"索引构建完成：{vectorstore._collection.count()} 个向量已存入 {config.CHROMA_DIR}")
