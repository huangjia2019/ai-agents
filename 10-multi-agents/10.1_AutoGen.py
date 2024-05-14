# 导入autogen包
import autogen

#配置大模型
llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": 'XXXXX'}],
}

# 定义鲜花电商的运营任务
inventory_tasks = [
    """查看当前库存中各种鲜花的数量，并报告哪些鲜花库存不足。""",
    """根据过去一个月的销售数据，预测接下来一个月哪些鲜花的需求量会增加。""",
]

market_research_tasks = ["""分析市场趋势，找出当前最受欢迎的鲜花种类及其可能的原因。"""]

content_creation_tasks = ["""利用提供的信息，撰写一篇吸引人的博客文章，介绍最受欢迎的鲜花及选购技巧。"""]

# 创建Agent角色
inventory_assistant = autogen.AssistantAgent(
    name="库存管理助理",
    llm_config llm_config,
)
market_research_assistant = autogen.AssistantAgent(
    name="市场研究助理",
    llm_config= llm_config,
)
content_creator = autogen.AssistantAgent(
    name="内容创作助理",
    llm_config= llm_config,
    system_message="""
        你是一名专业的写作者，以洞察力强和文章引人入胜著称。
        你能将复杂的概念转化为引人入胜的叙述。
        当一切完成后，请回复“结束”。
        """,
)

# 创建用户代理
user_proxy_auto = autogen.UserProxyAgent(
    name="用户代理_自动",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("结束"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
)

user_proxy = autogen.UserProxyAgent(
    name="用户代理",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("结束"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
)

# 发起对话
chat_results = autogen.initiate_chats(
    [
        {
            "sender": user_proxy_auto,
            "recipient": inventory_assistant,
            "message": inventory_tasks[0],
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": market_research_assistant,
            "message": market_research_tasks[0],
            "max_turns": 2,
            "summary_method": "reflection_with_llm",
        },
        {
            "sender": user_proxy,
            "recipient": content_creator,
            "message": content_creation_tasks[0],
            "carryover": "我希望在博客文章中包含一张数据表格或图表。",
        },
    ]
)


