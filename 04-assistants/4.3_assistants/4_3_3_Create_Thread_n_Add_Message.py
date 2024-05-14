# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 创建一个线程
thread = client.beta.threads.create()
# 打印线程
print(thread)

# 向线程添加消息
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="我把每个花束定价为进价基础上加价20%,进价80元时,我的售价是多少。"
)
# 打印消息
print(message)

