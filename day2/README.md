# Day 2 · LangChain 核心（12h）

目标：掌握 LCEL 管道链、消息占位、输出解析——LangChain 的三大地基概念。

## 学习要点（上午 4h）

- **LCEL（LangChain Expression Language）**：管道符 `|` 把"模板 → 模型 → 解析器"串成一条链，整条链像一个函数，可以 invoke / stream / batch
- **Runnable 三种调用**：invoke（一次性）、stream（流式，打字机效果）、batch（批量）
- **MessagesPlaceholder**：运行时把任意长度的历史消息塞进提示词（记忆的地基）
- **两种结构化输出方式**：D1 的 `with_structured_output(function_calling)`（靠模型原生工具能力）vs 本日 `PydanticOutputParser`（靠提示词指令 + 文本解析）

## 练习（下午 5h，按顺序做）

| 文件 | 练习 | 核心知识点 |
|---|---|---|
| 01_lcel_basics.py | LCEL 管道链 | invoke / stream / batch 对比 |
| 02_message_placeholder.py | 消息占位 | 动态历史消息（记忆地基） |
| 03_output_parser.py | 输出解析器 | 提示词指令 + JSON 文本解析 |
| 04_mini_qa.py | 知识问答链 | 知识注入 + 知识边界（RAG 雏形） |

运行方式：

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day2\01_lcel_basics.py
```

## 思考题（做完对照代码回答）

1. invoke / stream / batch 分别适合什么场景？（提示：聊天打字机效果用哪个？一次性处理 100 条用哪个？）
2. MessagesPlaceholder 相比 D1 手动 append 消息，优势是什么？
3. 练习 3 的 PydanticOutputParser 和 D1 的 function_calling 方式，底层差别是什么？（提示：一个靠"模型原生工具能力"，一个靠"提示词+文本解析"）
4. 练习 4 里"豆包怎么修电脑？"的回答说明了什么？把 temperature 从 0.2 改成 1.2 再跑一次，看回答会怎么变？

## 晚间（3h）

- 读官方概念文档：LCEL 与 Runnable
- 把 4 个练习各改造一个自己的版本
- 整理笔记：管道思维、三种调用方式、两种结构化输出

## 完成标准

- [ ] 4 个练习全部跑通
- [ ] 能不看代码画出一条"模板→模型→解析器"链，并说出三种调用方式
- [ ] 能说清两种结构化输出方式的差别
