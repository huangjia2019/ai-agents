# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

thread_id = 'thread_BORam4jiOCiPPpi4e0DR2pTJ' # 刚才创建的Thread的ID
run_id = 'run_yS0abDNBjzwyNzmse5a3GhUj' # 刚才创建的Run的ID

# 定义轮询间隔时间（例如：5秒）
polling_interval = 5

# 开始轮询Run的状态
import time
while True:
    run = client.beta.threads.runs.retrieve(
      thread_id=thread_id,
      run_id=run_id
    )
    
    # 直接访问run对象的属性
    status = run.status
    print(f"Run Status: {status}")
    
    # 如果 Run 的状态是 completed 或者 failed或者 expired，则退出循环
    if status in ['completed', 'failed', 'expired']:
        break
    
    # 等待一段时间再次轮询
    time.sleep(polling_interval)

# 运行完成或失败后处理结果
if status == 'completed':
    print("Run completed successfully.")
elif status == 'failed' or status == 'expired':
    print("Run failed or expired.")
