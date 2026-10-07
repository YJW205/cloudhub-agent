"""
练习 1：文档加载 + 文本分割 —— RAG 的第一步
目标：理解"长文档如何变成小块"：加载 → 分割（chunk）
运行：在项目根目录执行  python day4\\01_load_split.py
"""

from pathlib import Path

# 用标准库读文本文件（真实项目里常用 PDFLoader / DocxLoader 等专用加载器）
text = Path(__file__).resolve().parent / "knowledge" / "employee_manual.txt"
content = text.read_text(encoding="utf-8")
print(f"原始文档长度: {len(content)} 字\n")

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 分割器：按段落/句子递归切分，每块 200 字、重叠 50 字
# chunk_size 控制块大小（太长浪费 token，太短丢失上下文）
# chunk_overlap 让相邻块有重叠，避免"信息刚好被切在两块中间"
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
)
chunks = splitter.split_text(content)

print(f"分割后共 {len(chunks)} 块\n")
for i, chunk in enumerate(chunks[:3]):
    print(f"--- 第 {i+1} 块 ({len(chunk)} 字) ---")
    print(chunk)
    print()
