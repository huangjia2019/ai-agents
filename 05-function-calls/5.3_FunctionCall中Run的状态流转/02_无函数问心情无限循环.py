# 导入OpenAI库，并创建OpenAI客户端
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()

# 检索您之前创建的Assistant
assistant_id = "asst_pF2pMtIHOL4CpXpyUdHkoKG3" # 你自己的助手ID
assistant = client.beta.assistants.retrieve(assistant_id)
print(assistant)

# 创建一个新的Thread
thread = client.beta.threads.create()
print(thread)

# 向Thread添加用户的消息
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    # thread_id='thread_xSyXlruUzMIW1zD8rQUP3aFp',
    role="user",
    content="你好，请你安慰一下伤心的小雪吧！"
)
print(message)

# 运行Assistant来处理Thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)
print(run)

import time
# 轮询以检查Run的状态
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(run_status)
    if run_status.status == 'completed':
        break
    time.sleep(1)  # 等待1秒后再次检查

# 获取Assistant在Thread中的回应
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

# 输出Assistant的回应
for message in messages.data:
    if message.role == "assistant":
        print(message.content)