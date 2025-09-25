from dotenv import load_dotenv
load_dotenv()  

# 导入LangChain Hub
from langchain import hub
# 从hub中获取React的Prompt
prompt = hub.pull("hwchase17/react")
print(prompt)

# 导入ChatOpenAI
from langchain_community.llms import OpenAI
# 选择要使用的LLM
llm = OpenAI()

# 导入SerpAPIWrapper即工具包
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents.tools import Tool
# 实例化SerpAPIWrapper
search = SerpAPIWrapper()
# 准备工具列表
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="当大模型没有相关知识时，用于搜索知识"
    ),
]

# 导入create_react_agent功能
from langchain.agents import create_react_agent
# 构建ReAct代理
agent = create_react_agent(llm, tools, prompt)

# 导入AgentExecutor
from langchain.agents import AgentExecutor
# 创建代理执行器并传入代理和工具
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 调用代理执行器，传入输入数据
print("第一次运行的结果：")
agent_executor.invoke({"input": "当前Agent最新研究进展是什么?"})
print("第二次运行的结果：")
agent_executor.invoke({"input": "当前Agent最新研究进展是什么?"})