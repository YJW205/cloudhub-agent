"""
练习 4：第一个 Agent 雏形 —— 手动 Agent 循环（今天的重头戏）
目标：亲手实现"模型思考 → 调用工具 → 拿到结果 → 继续回答"的循环
运行：在项目根目录执行  python day3\\04_agent_assistant.py
      （这是交互式程序：输入问题回车，输入 exit 退出）
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-你的"):
    raise SystemExit("未找到有效的 DEEPSEEK_API_KEY，请先配置 .env 文件")

@tool
def multiply(a: int, b: int) -> int:
    """两个整数相乘。"""
    return a * b


@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气（模拟数据）。"""
    return f"{city}今天 25℃，多云"


# ===== 新增工具示例：汇率换算 =====
# 第一步：用 @tool 定义工具。参数必须带类型注解，docstring 描述用途和参数含义
@tool
def exchange_rates(amount: float, from_currency: str, to_currency: str) -> str:
    """按固定汇率换算金额。from_currency 是原始币种，to_currency 是目标币种。
    例：exchange_rates(100, "USD", "CNY") 表示把 100 美元换成人民币。"""
    rates = {"USD": 7.2, "EUR": 7.8, "JPY": 0.048, "CNY": 1.0}  # 模拟汇率表
    if from_currency.upper() not in rates or to_currency.upper() not in rates:
        return f"暂不支持，当前支持: {list(rates.keys())}"
    result = amount * rates[from_currency.upper()] / rates[to_currency.upper()]
    return f"{amount} {from_currency.upper()} ≈ {result:.2f} {to_currency.upper()}"

# ===== 新增工具示例：BMI 计算 =====
# 健康区间用中国成人标准（WS/T 428）：偏瘦 <18.5，正常 18.5~23.9，超重 24~27.9，肥胖 ≥28
@tool
def bmi(height_m: float, weight_kg: float) -> str:
    """返回 BMI 值和健康区间。height_m 是身高（米），weight_kg 是体重（公斤）。
    例：bmi(1.75, 70.0) 表示身高 1.75 米、体重 70 公斤。"""
    if height_m <= 0 or weight_kg <= 0:
        return "身高和体重都必须大于 0，请重新输入。"
    value = weight_kg / (height_m ** 2)
    if value < 18.5:
        level = "偏瘦"
    elif value < 24:
        level = "正常"
    elif value < 28:
        level = "超重"
    else:
        level = "肥胖"
    return f"BMI {value:.1f}，属于{level}区间"


# 第二步：注册进字典（循环里按名字调用工具）
tools = {
    "multiply": multiply,
    "get_weather": get_weather,
    "exchange_rates": exchange_rates,
    "bmi": bmi,          # 添加的11
}

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    temperature=0.3,
# 第三步：绑定给模型（模型才知道有这些工具可用）
).bind_tools([multiply, get_weather, exchange_rates, bmi])

print("=== AI 助手（输入 exit 退出）===")
# system 约束：降低工具调用出错的概率（源头缓解）
history = [SystemMessage(
    content="你是 AI 助手。规则：1) 一次只调用一个工具，完成后再调下一个；"
            "2) 调用工具前必须核对参数类型和格式；"
            "3) 数字参数必须是不带单位的纯数字（如 1.8，不要写成 1.8米）；"
            "4) 所有工具结果到齐后再统一回答。"
)]

while True:
    user_input = input("你: ")
    if user_input.lower() in ("exit", "quit"):
        break

    history.append(HumanMessage(content=user_input))

    # Agent 循环：模型可能要调用多次工具才给最终答案
    # 容错设计：工具调用失败不崩溃，把错误喂回模型，让它修正参数重试
    # 同时加最大轮数限制，防止极端情况下无限循环
    max_rounds = 5
    round_count = 0
    while True:
        round_count += 1
        if round_count > max_rounds:
            print("助手: 抱歉，工具调用次数过多，请换个说法再试。")
            break

        ai = llm.invoke(history)

        if ai.tool_calls:
            # 模型"申请"调用工具 → 追加它的请求，执行工具，把结果回传
            history.append(ai)
            for call in ai.tool_calls:
                try:
                    result = tools[call["name"]].invoke(call["args"])
                    print(f"  [调用工具 {call['name']} → 结果: {result}]")
                    history.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
                except Exception as e:
                    # 参数传错了 → 把错误回传模型，它会重新传参再试
                    print(f"  [工具 {call['name']} 调用失败: {e} → 已回传模型，等待重试]")
                    history.append(ToolMessage(
                        content=f"工具调用失败：{e}。请检查参数类型和名称后重试。",
                        tool_call_id=call["id"],
                    ))
        else:
            # 模型直接给出了最终回答
            print("助手:", ai.content)
            history.append(ai)
            break
