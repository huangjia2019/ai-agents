# 导入 OpenAI库
from openai import OpenAI

# 创建 OpenAI客户端
client = OpenAI()

# 调用chat.completions.create方法，得到响应
response = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "您是一个帮助用户了解鲜花信息的智能助手,并能够输出JSON格式的内容。"},
    {"role": "user", "content": "生日送什么花最好？"},
    {"role": "assistant", "content": "玫瑰是生日礼物的热门选择。"},
    {"role": "user", "content": "送货需要多长时间？"}
  ]
)

# 打印响应
print(response)