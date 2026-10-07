# Day 5 · LangGraph 图编排（12h）

目标：掌握 LangGraph（当前生产级 Agent 的主流框架），把 Day 3 的 Agent 和 Day 4 的 RAG 改造成"图"。

## 为什么用图？

Day 3 的手动 Agent 循环（while True）是"暗箱"：你无法从外部看到模型思考到哪一步。
LangGraph 把 Agent 变成**一张有向图**：每个环节是一个节点，节点间的流转清晰可见、
可中断（human-in-the-loop）、可持久化（checkpoint）——这是生产级 Agent 的标准形态。

## 学习要点（上午 4h）

- **State（状态）**：全图共享的"笔记本"，`Annotated[list, add_messages]` 表示追加而非覆盖
- **Node（节点）**：一个处理单元，输入 state 输出更新
- **Edge（边）**：`add_edge` 固定流转；`add_conditional_edges` 按路由函数动态选择
- **START / END**：图的入口和出口
- **ToolNode**：官方工具执行节点（替代 Day3 手写的执行循环）
- **Checkpointer**：自动保存每一步状态；`thread_id` 区分会话；SqliteSaver 持久化

## 练习（下午 5h，按顺序做）

| 文件 | 练习 | 核心知识点 |
|---|---|---|
| 01_state_graph.py | 图的基础 | State / Node / Edge / START / END |
| 02_conditional_routing.py | 条件路由 | 路由函数动态选边 |
| 03_memory_checkpoint.py | 官方记忆 | SqliteSaver + thread_id |
| 04_agent_graph.py | **Agent 图** | 把 Day3 循环改造成图（重头戏） |

运行方式：

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day5\01_state_graph.py
```

## 思考题（做完对照代码回答）

1. 01 里 `add_messages` 的作用是什么？去掉它会怎样？（提示：消息会被覆盖还是追加？）
2. 02 里路由函数返回的值，和 `add_conditional_edges` 的映射表是什么关系？
3. 03 里把 `thread_id` 从 `user_01` 改成 `user_02` 再问"我叫什么名字"，会怎样？为什么？
4. 04 和 Day3 的手写 while 循环比，图的好处是什么？（可观测 / 可持久化 / 可中断——至少说两点）

## 晚间（3h）

- 读官方教程：<https://docs.langchain.com/oss/python/langgraph/quickstart>
- 把 Day4 的 RAG 链改造成图（一个 agent 节点 + 条件路由：问题→检索→回答）
- 为 Day6 项目画一张架构草图（提示：agent 节点 / 工具节点 / 检索节点 / 记忆）

## 完成标准

- [ ] 4 个练习全部跑通
- [ ] 能口述 LangGraph 五要素（State/Node/Edge/条件路由/Checkpointer）
- [ ] 能说出"图 vs 手写循环"至少三个优势
