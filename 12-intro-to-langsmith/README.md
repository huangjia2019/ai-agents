# Intro to LangSmith

Welcome to Intro to LangSmith!

## Introduction
In this course we will walk through the fundamentals of LangSmith - exploring observability, prompt engineering, evaluations, feedback mechanisms, and production monitoring. Take a look at the setup instructions below so you can follow along with any of our notebook examples.

---

## Setup
Follow these instructions to make sure you have all the resources necessary for this course!

### Sign up for LangSmith
* Sign up [here](https://smith.langchain.com/) 
* Navigate to the Settings page, and generate an API key in LangSmith.
* Create a .env file that mimics the provided .env.example. Set `LANGCHAIN_API_KEY` in the .env file.

### Set OpenAI API key
* If you don't have an OpenAI API key, you can sign up [here](https://openai.com/index/openai-api/).
* Set `OPENAI_API_KEY` in the .env file.

### Create an environment and install dependencies
```
$ cd intro-to-langsmith
$ python3 -m venv intro-to-ls
$ source intro-to-ls/bin/activate
$ pip install -r requirements.txt
```

### Self-Hosted LangSmith
Note: If you are using a self-hosted version of LangSmith, you'll need to set this environment variable in addition to the others - see this [guide](https://docs.smith.langchain.com/self_hosting/usage) for more info
```
LANGSMITH_ENDPOINT = "<your-self-hosted-url>/api/v1"
```
