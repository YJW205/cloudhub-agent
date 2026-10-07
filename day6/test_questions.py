"""
test_questions.py —— 项目自测脚本（非交互，验证图各环节）
覆盖四类问题：文档问答 / 费用计算 / 故障排查 / 知识边界
运行：python day6\\test_questions.py
"""

import config
from app import build_app

app = build_app()
cfg = {"configurable": {"thread_id": "test_session"}}

questions = [
    "专业版每人每月多少钱？",                      # → retrieve（文档问答）
    "企业版 20 个席位按年付费一年要多少钱？",      # → subscription_cost（工具计算）
    "Webhook 收不到回调怎么排查？",                # → retrieve（故障排查）
    "今天佛山天气怎么样？",                        # → 知识边界（文档外）
]

for q in questions:
    result = app.invoke({"messages": [("human", q)]}, config=cfg)
    answer = result["messages"][-1].content
    print(f"Q: {q}")
    print(f"A: {answer}")
    print("-" * 60)
