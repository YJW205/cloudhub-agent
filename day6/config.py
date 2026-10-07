"""
config.py —— 项目公共配置
所有脚本共用的路径与 API Key 加载
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录（day6 的上级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 加载根目录 .env 里的 DEEPSEEK_API_KEY
load_dotenv(PROJECT_ROOT / ".env")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# embedding 模型缓存（与 Day4 共用，避免重复下载）
os.environ.setdefault("HF_HOME", str(PROJECT_ROOT / "models"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 路径常量
KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge" / "saas_product_docs.txt"
CHROMA_DIR = str(PROJECT_ROOT / "chroma_db")        # 知识库索引（与 Day4 同一向量库）
CHECKPOINT_DB = "E:/ai/doubao project/agent_checkpoints.db"  # 记忆数据库

EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"
LLM_MODEL = "deepseek-chat"
LLM_BASE_URL = "https://api.deepseek.com"

# 工具容错：最多允许模型连续调用工具的轮数
MAX_TOOL_ROUNDS = 6
