# Day 6 · 项目冲刺：云枢 CloudHub 产品文档助手

今天产出你的**简历项目**。所有能力合体：RAG（Day4）+ 工具（Day3）+ 记忆（Day5）+ LangGraph 图编排。

## 项目架构

```
用户问题 → START
              ↓
         agent（模型思考）—— 有条件路由：
              ↓ 有 tool_calls          ↓ 无 tool_calls
        tools（执行工具）───→ agent    END（回答）
           │
           ├─ retrieve：Chroma 知识库检索（Agentic RAG，模型自主决定何时查文档）
           └─ subscription_cost：套餐费用计算
    + SqliteSaver checkpoint：多轮记忆（thread_id）
```

**核心亮点（面试必讲）：Agentic RAG**
不是"所有问题都先检索"的固定流程，而是把"检索"做成一个工具，**让模型自己判断**：
- 问产品功能/价格 → 模型主动调用 retrieve
- 问费用计算 → 模型调用 subscription_cost
- 闲聊/文档外问题 → 模型直接回答或说明未找到

## 运行步骤

```powershell
cd "E:\ai\doubao project"
.\.venv\Scripts\Activate.ps1
python day6\build_index.py      # 1. 构建知识库索引（只需一次）
python day6\app.py              # 2. 启动交互式助手
python day6\test_questions.py   # 3. 自测脚本（验证四类问题）
```

## 测试问题清单（对着验证）

| 问题 | 预期行为 |
|---|---|
| 专业版每人每月多少钱？ | 调用 retrieve → 答 89 元/席位 |
| 企业版 20 个席位按年付一年多少钱？ | 调用 subscription_cost → 299×20×12×0.8 |
| Webhook 收不到回调怎么排查？ | 调用 retrieve → 按文档答 HTTPS+公网+测试按钮 |
| 今天佛山天气怎么样？ | 不检索、不算账 → 明确"文档中未找到"（知识边界） |
| 连续问 2-3 个问题后换话题 | checkpoint 记忆上下文（多轮） |

## 想挑战加分项（可选）

1. **给助手加一个工具**：如 `check_api_error(code)` 查错误码含义（文档里有 400/401/429/500）
2. **记录引用**：让 retrieve 返回资料块编号，回答时标注"（来源：API 文档）"
3. **换自己的文档**：把你的真实 SaaS/技术文档放 knowledge/ 替换，重跑 build_index

## 完成标准

- [ ] build_index 跑通，索引建立
- [ ] app.py 交互问答正常，四类问题行为符合预期
- [ ] 能向别人讲清"Agentic RAG + 工具 + 记忆"的架构
- [ ] （加分）加了一个自己的业务工具
