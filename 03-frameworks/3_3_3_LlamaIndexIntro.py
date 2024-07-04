# 读取系统变量
from dotenv import load_dotenv
load_dotenv()  

# 从指定目录读取文档数据
from llama_index.core import SimpleDirectoryReader  
documents = SimpleDirectoryReader(r"03-frameworks\data").load_data()

# 使用读取到的文档数据创建向量存储索引
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)

# 将索引转换为查询引擎Agent
agent = index.as_query_engine()

# 查询并打印结果
response = agent.query("花语秘境的员工有几处角色?")
print("花语秘境的员工有几处角色?", response)
response = agent.query("花语秘境的Agent叫啥名字")
print("花语秘境的Agent叫啥名字",response)

# 将索引的存储上下文持久化
index.storage_context.persist()