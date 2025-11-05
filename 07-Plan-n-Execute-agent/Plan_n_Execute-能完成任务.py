# 设置OpenAI网站和SerpApi网站提供的API密钥
from dotenv import load_dotenv  # 用于加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

# 导入LangChain 工具
from langchain.tools import tool

# 库存查询
@tool
def check_inventory(flower_type: str) -> int:
    """
    查询特定类型花的库存数量。
    参数:
    - flower_type: 花的类型
    返回:
    - 库存数量 (暂时返回一个固定的数字)
    """
    # 实际应用中这里应该是数据库查询或其他形式的库存检查
    return 100  # 假设每种花都有100个单位

# 定价函数
@tool
def calculate_price(base_price: float, markup: float) -> float:
    """
    根据基础价格和加价百分比计算最终价格。
    参数:
    - base_price: 基础价格
    - markup: 加价百分比
    返回:
    - 最终价格
    """
    return base_price * (1 + markup)

# 调度函数
@tool
def schedule_delivery(order_id: int, delivery_date: str):
    """
    安排订单的配送。
    参数:
    - order_id: 订单编号
    - delivery_date: 配送日期
    返回:
    - 配送状态或确认信息
    """
    # 在实际应用中这里应该是对接配送系统的过程
    return f"订单 {order_id} 已安排在 {delivery_date} 配送"
tools = [check_inventory, calculate_price, schedule_delivery]

# 设置大模型
from langchain.chat_models import ChatOpenAI
model = ChatOpenAI(temperature=0)

# 设置计划者和执行者
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)

# 初始化Plan-and-Execute Agent
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# 运行Agent解决新问题（完善了需求）
agent.run("查查玫瑰的库存然后给出50朵玫瑰的价格和当天的配送方案！")


