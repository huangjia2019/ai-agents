# LangSmith 入门指南

欢迎来到 LangSmith 入门指南！

## 介绍
在这个课程中，我们将学习 LangSmith 的基础知识 - 探索可观测性、提示工程、评估、反馈机制和生产监控。请查看下面的设置说明，以便您可以跟随我们的任何笔记本示例。

---

## 设置
按照这些说明确保您拥有本课程所需的所有资源！

### 注册 LangSmith
* 在[这里](https://smith.langchain.com/)注册
* 导航到设置页面，在 LangSmith 中生成 API 密钥。
* 创建一个模仿提供的 .env.example 的 .env 文件。在 .env 文件中设置 `LANGCHAIN_API_KEY`。

### 设置 OpenAI API 密钥
* 如果您没有 OpenAI API 密钥，可以在[这里](https://openai.com/index/openai-api/)注册。
* 在 .env 文件中设置 `OPENAI_API_KEY`。

### 创建环境并安装依赖项
```
$ cd intro-to-langsmith
$ python3 -m venv intro-to-ls
$ source intro-to-ls/bin/activate
$ pip install -r requirements.txt
```

### 自托管 LangSmith
注意：如果您使用的是自托管版本的 LangSmith，除了其他环境变量外，您还需要设置此环境变量 - 请参阅此[指南](https://docs.smith.langchain.com/self_hosting/usage)了解更多信息
```
LANGSMITH_ENDPOINT = "<your-self-hosted-url>/api/v1"
```