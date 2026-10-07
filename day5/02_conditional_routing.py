"""
练习 2：条件路由 —— 让图自己决定走哪条路
目标：理解 add_conditional_edges：路由函数根据 state 内容动态选择下一个节点
      这就是 Day4 RAG 里"要不要检索"、Day3 Agent 里"继续调工具还是回答"的底层机制
运行：在项目根目录执行  python day5\\02_conditional_routing.py
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str  # 用户想聊的话题

def analyst_node(state: State):
    return {"topic": f"分析师视角：我们来深度分析『{state['topic']}』"}


def coder_node(state: State):
    return {"topic": f"程序员视角：我来写『{state['topic']}』相关的代码"}


def route(state: State):
    """路由函数：返回下一步要去的节点名（必须在映射表里存在）"""
    if state["topic"] == "python":
        return "coder"
    return "analyst"


graph = StateGraph(State)
graph.add_node("analyst", analyst_node)
graph.add_node("coder", coder_node)

# 关键：条件边 —— START 之后走哪个节点，由 route 函数说了算
graph.add_conditional_edges(
    START,
    route,
    {"analyst": "analyst", "coder": "coder"},  # route 返回值 → 节点名 的映射
)
graph.add_edge("analyst", END)
graph.add_edge("coder", END)

app = graph.compile()

for topic in ["python", "经济学", "python", "电影"]:
    result = app.invoke({"topic": topic})
    print(f"话题『{topic}』→ {result['topic']}")
