# 读取系统变量
from dotenv import load_dotenv
load_dotenv()  

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader  
documents = SimpleDirectoryReader("03-frameworks\docs").load_data()

index = VectorStoreIndex.from_documents(documents)

agent = index.as_query_engine()

response = agent.query("花语秘境的员工有几处角色?")
print("花语秘境的员工有几处角色?", response)
response = agent.query("花语秘境的Agent叫啥名字")
print("花语秘境的Agent叫啥名字",response)

index.storage_context.persist()