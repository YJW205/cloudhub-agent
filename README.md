# 云枢 CloudHub 产品文档助手

目标：7 天 × 12 小时，熟悉 LangChain / LangGraph，完成一个可写进简历的 Agent 项目。

## 项目结构

```
E:\ai\doubao project\
├── .venv\                  # Python 3.12 虚拟环境（所有依赖都装在这里）
├── .env.example            # API Key 配置模板（复制为 .env 后填入真实 Key）
├── day1\                   # LLM API 基础
├── day2\                   # LangChain 核心（提示模板 / 输出解析 / LCEL）
├── day3\                   # 工具调用 + 记忆
├── day4\                   # RAG + 项目定题
├── day5\                   # LangGraph 图编排
├── day6\                   # 项目冲刺
└── day7\                   # 复盘 + 简历 + 面试
```

## 环境说明

- Python 版本：3.12.14（虚拟环境内）
- 虚拟环境路径：`E:\ai\doubao project\.venv`
- 已安装：langchain 1.4.3、langchain-openai 1.6.7、langchain-community 0.4.2、langgraph 1.2.14、python-dotenv、chromadb、langchain-chroma

### 激活虚拟环境（每次打开终端都要做）

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
```

激活后命令行前面会出现 `(.venv)` 前缀。看到 `python --version` 输出 3.12 即成功。

> 如果提示"禁止运行脚本"，先执行：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 配置 API Key（今天第一步）

1. 打开 <https://platform.deepseek.com> 注册账号，进入「API Keys」创建 Key（新用户送额度，不够再充 10 元够用很久）
2. 复制 `E:\ai\doubao project\.env.example` 为 `.env`
3. 把 Key 粘贴进 `.env` 文件：`DEEPSEEK_API_KEY=sk-你的key`

## 每日使用方式

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day1\01_hello_api.py     # 运行当日练习
```

每天写完练习后，把代码发给豆包 Review，再进入下一天。

## Day 6 · 简历项目：云枢产品文档助手

```powershell
python day6\build_index.py      # 构建知识库索引（只需一次）
python day6\app.py              # 启动交互式助手（输入 exit 退出）
python day6\test_questions.py   # 四类问题自测
```

- 架构：LangGraph 图编排 Agentic RAG（检索/费用计算/错误码三个工具 + SqliteSaver 记忆）
- 详细说明见 `day6\README.md`

## Day 7 · 复盘 / 简历 / 面试

| 文件 | 用途 |
|---|---|
| `day7\01_项目复盘.md` | 项目架构 + 技术决策 + 踩坑清单（面试讲稿底稿） |
| `day7\02_简历项目描述.md` | 简历项目经验条目（完整版 / 精简版 / 口播版） |
| `day7\03_面试模拟.md` | 30 道高频题 + 参考答案 + 自测方法 |
