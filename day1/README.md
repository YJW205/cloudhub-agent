# Day 1 · LLM API 基础（12h）

目标：理解大模型 API 的调用方式与核心概念，为 LangChain 打地基。

## 学习要点（上午 4h）

- **消息结构**：system（设定角色）/ user（用户输入）/ assistant（模型回复）
- **核心参数**：temperature（随机性）、max_tokens（输出上限）
- **token 是什么**：模型计费与上下文窗口的基本单位，中文约 1 字 ≈ 1.5~2 token
- 注册 DeepSeek 并拿到 API Key（`platform.deepseek.com`）

## 练习（下午 5h，按顺序做）

| 文件 | 练习 | 核心知识点 |
|---|---|---|
| 01_hello_api.py | 第一次调用 | invoke 用法、AIMessage 结构 |
| 02_system_prompt.py | 角色控制 + 参数 | system prompt、temperature 对比 |
| 03_json_output.py | 结构化输出 | Pydantic schema、with_structured_output |
| 04_multi_turn.py | 多轮对话 | 消息序列累积（记忆的地基） |

运行方式（在项目根目录）：

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day1\01_hello_api.py
```

## 每个练习做完后的思考题

- 01：`invoke()` 返回的是什么对象？`.content` 是什么类型？
- 02：temperature=0 和 1.5 的回答有什么差别？什么场景该用低温度？
- 03：如果模型返回的 JSON 不符合 schema 会怎样？试着故意让它返回错误格式
- 04：把第 2 轮的对话历史去掉再问一次，看模型是否还记得之前的安排？

## 晚间（3h）

- 通读官方概念文档：<https://docs.langchain.com/oss/python/langchain/quickstart>
- 整理今日笔记：消息结构、参数、结构化输出（这三点是后面所有内容的地基）
- 把 4 个练习各改造一个自己的版本（比如换成你感兴趣的主题）

## 完成标准

- [ ] 4 个练习全部跑通，且能解释每行代码的作用
- [ ] 不用看代码，能口述"一次 API 调用"的完整流程
