# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 创建一个Run
run = client.beta.threads.runs.create(
  thread_id='thread_BORam4jiOCiPPpi4e0DR2pTJ',
  assistant_id='asst_z37EZbDPHq6ycDK66OFMjor2',
  instructions="请回答问题." # 如果你希望覆盖原有的指令
)
# 打印Run
print(run)

# 再次获取Run的状态
run = client.beta.threads.runs.retrieve(
  thread_id='thread_BORam4jiOCiPPpi4e0DR2pTJ',
  run_id=run.id
)
# 打印Run
print(run)