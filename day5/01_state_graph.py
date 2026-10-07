"""
练习 1：LangGraph 基础 —— State、Node、Edge
目标：理解"图"的三个要素：状态(State)、节点(Node)、边(Edge)
      图 = 有向图，数据从 START 流向 END，节点之间通过边连接
运行：在项目根目录执行  python day5\\01_state_graph.py
"""

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# State：全图共享的"笔记本"。这里存消息列表，
# add_messages 注解表示"新消息追加到已有列表"（而不是覆盖）
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Node：一个处理单元。输入 state，返回 state 的"更新"（部分字段）
def greet_node(state: State):
    return {"messages": [("ai", "你好！我是图里的第一个节点。")]}


def farewell_node(state: State):
    return {"messages": [("ai", "再见！你走到了终点 END。")]}


# 构图：注册节点 + 连边
# START 是图的入口，END 是出口
graph = StateGraph(State)
graph.add_node("greet", greet_node)
graph.add_node("farewell", farewell_node)
graph.add_edge(START, "greet")
graph.add_edge("greet", "farewell")
graph.add_edge("farewell", END)

# 编译成可执行对象（compile 之后才能 invoke）
app = graph.compile()

# 运行：从 START 进入，一路流过 greet → farewell → END
result = app.invoke({"messages": [("human", "开始")]})
print("消息流转过程：")
for msg in result["messages"]:
    print(f"  [{msg.type}] {msg.content}")
