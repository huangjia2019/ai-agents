# 此仓库中的智能体

## 概述

该仓库演示了使用 LangGraph 构建智能体，专注于一个能够：
- 对收件邮件进行分类
- 起草适当的回复
- 执行操作（日历安排等）
- 融合人工反馈
- 从过去的交互中学习

的电子邮件助手。

## 环境设置

**推荐：使用 uv（更快更可靠）**

```bash
# 如果还没有安装 uv
pip install uv

# 安装带有开发依赖的包
uv sync --extra dev
```

**替代方案：使用 pip**

```bash
# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 确保您有最新版本的 pip（带有 pyproject.toml 的可编辑安装需要）
python3 -m pip install --upgrade pip

# 以可编辑模式安装包
pip install -e .
```

包安装为 `interrupt_workshop`，导入名称为 `email_assistant`，允许您使用 `from email_assistant import ...` 从任何地方导入

## 智能体实现

### 脚本

该仓库在 `src/email_assistant` 中包含几个复杂度递增的实现：

1. **LangGraph 101** (`langgraph_101.py`)
   - LangGraph 的基础知识

2. **基本电子邮件助手** (`email_assistant.py`)
   - 核心电子邮件分类和响应功能

3. **人工干预** (`email_assistant_hitl.py`)
   - 添加人类审查和批准操作的能力

4. **启用记忆的 HITL** (`email_assistant_hitl_memory.py`)
   - 添加持久记忆以从反馈中学习

5. **Gmail 集成** (`email_assistant_hitl_memory_gmail.py`)
   - 连接到 Gmail API 进行真实的电子邮件处理

### Notebook

智能体的每个方面都在专门的 notebook 中解释：
- `notebooks/langgraph_101.ipynb` - LangGraph 基础知识
- `notebooks/agent.ipynb` - 基本智能体实现
- `notebooks/evaluation.ipynb` - 智能体评估
- `notebooks/hitl.ipynb` - 人工干预功能
- `notebooks/memory.ipynb` - 添加记忆能力

## 运行测试

### 测试脚本

测试以确保所有实现工作：

```bash
# 测试所有实现
python tests/run_all_tests.py --all
```

（注意：这将从测试中排除 Gmail 实现 `email_assistant_hitl_memory_gmail`。）

### 测试 Notebook

测试所有 notebook 以确保它们运行没有错误：

```bash
# 直接运行所有 notebook 测试
python tests/test_notebooks.py
```