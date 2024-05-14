# 导入所需的库
from langchain_core.output_parsers import StrOutputParser # 用于解析输出结果为字符串
from langchain_core.prompts import ChatPromptTemplate # 用于创建聊天提示模板
from langchain_openai import ChatOpenAI # 用于调用OpenAI的GPT模型

# 创建一个聊天提示模板，其中{topic}是一个占位符，用于后续插入具体的话题
prompt = ChatPromptTemplate.from_template("请讲一个关于 {topic} 的故事")
# 初始化ChatOpenAI对象，指定使用的模型为"gpt-4"
model = ChatOpenAI(model="gpt-4")
# 初始化一个输出解析器，用于将模型的输出解析成字符串
output_parser = StrOutputParser()

'''使用管道操作符（|）连接各个处理步骤，创建一个处理链
   其中prompt用于生成具体的提示文本，
   model用于根据提示文本生成回应，
   output_parser用于处理回应并将其转换为字符串''' 
chain = prompt | model | output_parser

# 调用处理链，传入话题"水仙花"，执行生成故事的操作
message = chain.invoke({"topic": "水仙花"})

# 打印链的输出结果
print(message)