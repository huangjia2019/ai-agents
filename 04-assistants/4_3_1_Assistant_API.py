# 导入环境变量
from dotenv import load_dotenv 
load_dotenv()
# 创建 client
from openai import OpenAI 
client = OpenAI()
# 创建 assistant
assistant = client.beta.assistants.create(
    name=" 鲜花价格计算器 ",
    instructions=" 你能够帮我计算鲜花的价格 ", tools=[{"type": "code_interpreter"}], model="gpt-4-turbo-preview"
    )
# 打印 assistant print(assistant)
print(assistant)