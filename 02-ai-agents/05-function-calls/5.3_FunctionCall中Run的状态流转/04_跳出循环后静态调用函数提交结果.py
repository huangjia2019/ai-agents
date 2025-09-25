# 读取系统变量
from dotenv import load_dotenv
load_dotenv()  

from openai import OpenAI
# 初始化客户端
client = OpenAI()

# 检索您之前创建的Assistant
assistant_id = "asst_pF2pMtIHOL4CpXpyUdHkoKG3" # 你自己的助手ID
# thread_id = 'thread_ZBhfduW0rklxu120EnIH0QZT'

# 创建一个新的Thread
thread = client.beta.threads.create()
print(thread)
thread_id = thread.id

# 向Thread添加用户的消息
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    # thread_id='thread_xSyXlruUzMIW1zD8rQUP3aFp',
    role="user",
    content="快安慰一下伤心的小雪！"
)
print(message)

# 运行Assistant来处理Thread
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id
)
print(run)

# 轮询Run，从Queue到'requires_action'
import time
# 定义一个轮询的函数
def poll_run_status(client, thread_id, run_id, interval=2):
    """ 轮询Run的状态，直到它不再是'requires_action'或直到完成 """
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, 
                                                       run_id=run_id)
        print(run)
        if run.status in ['requires_action', 'completed']:
            return run
        time.sleep(interval)  # 等待后再次检查

# 轮询以检查Run的状态
print('这时，Run应该是进入了requires_action状态')
run = poll_run_status(client, thread_id, run.id)
print(run)


# 读取function元数据信息
def get_function_details(run):

#   print("\nrun.required_action\n",run.required_action)

  function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
  arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
  function_id = run.required_action.submit_tool_outputs.tool_calls[0].id

#   print(f"function_name: {function_name} and arguments: {arguments}")

  return function_name, arguments, function_id

# 读取并打印元数据信息
function_name, arguments, function_id = get_function_details(run)
print("function_name:", function_name)
print("arguments:", arguments)
print("function_id:", function_id)

# 再次打印Run的状态
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
print("读取function元数据信息之后Run的状态",run)


# 定义鼓励函数
def get_encouragement(mood, name=None):
    encouragement_messages = {
        "开心": "看到你这么阳光真好！保持这份积极！",
        "难过": "记得，每片乌云背后都有阳光。",
        "压力大": "深呼吸，慢慢呼出，一切都会好起来的。",
        "疲倦": "你已经很努力了，现在是时候休息一下了。"
    }

    # 如果提供了名字，个性化消息
    if name:
        message = f"{name}，{encouragement_messages.get(mood, '抬头挺胸，一切都会变好的。')}"
    else:
        message = encouragement_messages.get(mood, '抬头挺胸，一切都会变好的。')

    return message


# 根据Assistant返回的参数动态调用鼓励函数
import json

# 将 JSON 字符串转换为字典
arguments_dict = json.loads(arguments)

# 从字典中提取 'name' 和 'mood'
name = arguments_dict['name']
mood = arguments_dict['mood']

# 调用函数
encouragement_message = get_encouragement(name, mood)

# 打印结果以进行验证
print(encouragement_message)

# 再次打印Run的状态
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
print("提交结果之前Run的状态",run)

# 提交结果
def submit_tool_outputs(run,thread,function_id,function_response):
    run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
      {
        "tool_call_id": function_id,
        "output": str(function_response),
      }
    ]
    ) 
    return run

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

run = submit_tool_outputs(run,thread,function_id,'Function Calling 结束！')
print("提交结果之后Run的状态",run)

# 获取Assistant在Thread中的回应
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print("全部的message", messages)