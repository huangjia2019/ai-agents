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

# 轮询Run，从'queue'等到'requires_action'
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

# 定义一个从Run中读取Function信息的函数
def get_function_details(run):
  
  function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
  arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
  function_id = run.required_action.submit_tool_outputs.tool_calls[0].id 

  return function_name, arguments, function_id

# 拿到Function的元数据信息
function_name, arguments, function_id = get_function_details(run)
print("function_name:", function_name)
print("arguments:", arguments)
print("function_id:", function_id)

# 再次检查Run的状态 - 不需要轮询 -- 一直是Queue
print('这时，Run已经从requires_action出来了')
run = client.beta.threads.runs.retrieve(thread_id=thread_id, 
                                                run_id=run.id)
print(run)

# 定义鼓励函数
def get_encouragement(name, mood):
    # 基础鼓励消息
    messages = {
        "happy": "继续保持积极的心态，做得好！",
        "sad": "记住，即使在最黑暗的日子里，也会有阳光等待着你。",
        "tired": "你做得足够好了，现在是时候休息一下了。",
        "stressed": "深呼吸，一切都会好起来的。"
    }
    
    # 获取对应心情的鼓励消息
    message = messages.get(mood.lower(), "你今天感觉如何？我总是在这里支持你！")
    
    # 返回定制化的鼓励消息
    return f"亲爱的{name}，{message}"

# ---- 这里，我可要动态调用程序了！！！
import json

# 定义可用的函数字典
available_functions = {
    "get_encouragement": get_encouragement
}

# 解析参数
function_args = json.loads(arguments)

# 动态调用函数
function_to_call = available_functions[function_name]
encouragement_message = function_to_call(
    name=function_args.get("name"),
    mood=function_args.get("mood")
)

# 打印结果以进行验证
print(encouragement_message)

# 向Run提交结果
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

run = submit_tool_outputs(run,thread,function_id,encouragement_message)
print('这时，Run收到了结果')
print(run)

print('这时，Run继续执行直至完成')
# 再次轮询Run直至完成
run = poll_run_status(client, thread_id, run.id) 
print(run)

# 获取Assistant在Thread中的回应
messages = client.beta.threads.messages.list(
  thread_id=thread_id
)

# 输出Assistant的回应
print('下面打印最终的Message')
for message in messages.data:
    if message.role == "assistant":
        print(message.content)