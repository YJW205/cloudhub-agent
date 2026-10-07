# Day 3 · 工具调用 + 记忆（12h）

目标：让 Agent 拥有"手脚"（工具）和"记忆"（对话历史），组装出第一个 Agent 雏形。

## 学习要点（上午 4h）

- **@tool**：把普通函数变成模型可调用的工具（name / description / args 三个字段）
- **bind_tools**：把工具绑定到模型，模型"知道"有这些工具可用
- **tool_calls**：模型不直接回答，而是"申请"调用工具 —— 执行权在你的代码手里
- **ToolMessage**：把工具执行结果回传给模型，模型才能继续回答
- **持久化记忆**：SQLiteChatMessageHistory 把历史存磁盘，重启不丢

## 练习（下午 5h，按顺序做）

| 文件 | 练习 | 核心知识点 |
|---|---|---|
| 01_define_tool.py | 定义工具 | @tool、工具的 schema |
| 02_tool_calling.py | 模型申请调工具 | bind_tools、tool_calls |
| 03_memory.py | 持久化记忆 | 标准库 sqlite3 存取（LangGraph checkpointer 的底层原理） |
| 04_agent_assistant.py | **Agent 雏形** | 手动 Agent 循环（重头戏） |

运行方式：

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day3\01_define_tool.py
```

**注意：练习 4 是交互式程序**，运行后输入问题回车，输入 `exit` 退出。

## 思考题（做完对照代码回答）

1. 工具的 name / description / args 三个字段分别起什么作用？模型靠哪个字段决定"要不要调用这个工具"？（提示：description）
2. bind_tools 之后，模型输出 tool_calls 意味着什么？为什么说"执行权在你手里"？
3. 练习 3 的 SQLite 持久化和 D1 手动 append 消息，本质差别是什么？（进程内存 vs 磁盘，重启后是否还在）
4. 练习 4 里为什么循环要反复 invoke，直到模型不再调用工具？（提示：一个任务可能需要连续调用多次工具，比如"算完乘法再查天气"）

## 晚间（3h）

- 在练习 4 里**新增你自己的工具**（比如：查询数据库、计算 BMI、汇率换算），让助手功能更多
- 想一想：如果想让模型能"循环 10 次工具调用"，代码需要怎么改？如果工具调用无限循环怎么办？
- 整理笔记：工具调用的完整链路（模型 → tool_calls → 执行 → ToolMessage → 模型）

## 完成标准

- [ ] 4 个练习全部跑通，练习 4 能交互对话
- [ ] 能口述"Agent 工具调用"的完整循环链路
- [ ] 给助手加了一个自己的新工具并成功使用
