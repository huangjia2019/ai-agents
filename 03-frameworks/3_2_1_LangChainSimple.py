# 导入dotenv包，用于加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入langchain_openai库中的OpenAI类，用于与OpenAI进行交互
from langchain_openai import OpenAI
# 导入langchain_community.llms中的Cohere和HuggingFaceHub类，用于使用Cohere和HuggingFace的模型
from langchain_community.llms import Cohere, HuggingFaceHub

# 初始化OpenAI、Cohere和HuggingFaceHub的实例，并设置温度参数（控制生成文本的创新性）
openai = OpenAI(temperature=0.1)
cohere = Cohere(model="command", temperature=0.1)
huggingface = HuggingFaceHub(repo_id="tiiuae/falcon-7b", model_kwargs={'temperature':0.1})

# 导入ModelLaboratory类，用于创建和管理多个语言模型
from langchain.model_laboratory import ModelLaboratory

# 创建一个模型实验室实例，整合了OpenAI、Cohere和HuggingFace的模型
model_lab = ModelLaboratory.from_llms([openai, cohere, huggingface])

# 使用模型实验室比较不同模型对同一个问题“百合花是来源自哪个国家?”的回答
model_lab.compare("百合花是来源自哪个国家?")

