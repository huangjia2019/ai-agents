# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 检索您之前创建的Assistant
assistant_id = "asst_pF2pMtIHOL4CpXpyUdHkoKG3" # 你自己的助手ID
assistants = client.beta.assistants.list()
print(assistants)