# 🧱 从零开始构建深度智能体

<img width="720" height="289" alt="Screenshot 2025-08-12 at 2 13 54 PM" src="https://github.com/user-attachments/assets/90e5a7a3-7e88-4cbe-98f6-5b2581c94036" />

[深度研究](https://academy.langchain.com/courses/deep-research-with-langgraph)与编程一起成为首批主要的智能体应用场景之一。现在，我们看到了可用于广泛任务的通用智能体的兴起。例如，[Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) 在长期任务方面获得了显著关注和流行度；平均每个 Manus 任务使用约50次工具调用！作为第二个例子，Claude Code 被广泛用于编程之外的任务。仔细审查这些流行"深度"智能体的[上下文工程模式](https://docs.google.com/presentation/d/16aaXLu40GugY-kOpqDU4e-S0hD1FmHcNyF0rRRnb1OU/edit?slide=id.p#slide=id.p)显示了一些共同方法：

* **任务规划（例如，TODO），通常伴随重述**
* **上下文卸载到文件系统**
* **通过子智能体委托进行上下文隔离**

本课程将展示如何使用 LangGraph 从零开始实现这些模式！

## 🚀 快速开始

### 前置条件

- 确保您使用的是 Python 3.11 或更高版本。
- 此版本是与 LangGraph 最佳兼容性所必需的。
```bash
python3 --version
```
- [uv](https://docs.astral.sh/uv/) 包管理器
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 更新 PATH 以使用新的 uv 版本
export PATH="/Users/$USER/.local/bin:$PATH"
```

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/langchain-ai/deep_agents_from_scratch
cd deep_agents_from_scratch
```

2. 安装包和依赖项（这会自动创建和管理虚拟环境）：
```bash
uv sync
```

3. 在项目根目录创建 `.env` 文件并添加您的 API 密钥：
```bash
# 创建 .env 文件
touch .env
```

将您的 API 密钥添加到 `.env` 文件中：
```env
# 具有外部搜索功能的研究智能体所需
TAVILY_API_KEY=your_tavily_api_key_here

# 模型使用所需
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 可选：用于评估和跟踪
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=deep-agents-from-scratch
```

4. 使用 uv 运行笔记本或代码：
```bash
# 直接运行 Jupyter 笔记本
uv run jupyter notebook

# 或者如果喜欢，激活虚拟环境
source .venv/bin/activate  # Windows 系统：.venv\Scripts\activate
jupyter notebook
```

## 📚 教程概览

本仓库包含五个渐进式笔记本，教您构建高级 AI 智能体：

### `0_create_agent.ipynb` -
学习如何使用 create_agent 组件。此组件：
- 实现了 ReAct（推理-行动）循环，这是许多智能体的基础。
- 易于使用且快速设置。
- 作为基础

### `1_todo.ipynb` - 任务规划基础
学习使用 TODO 列表实现结构化任务规划。本笔记本介绍：
- 带状态管理的任务跟踪（待处理/进行中/已完成）
- 进度监控和上下文管理
- 用于组织复杂多步骤工作流的 `write_todos()` 工具
- 保持专注和防止任务偏移的最佳实践

### `2_files.ipynb` - 虚拟文件系统
实现存储在智能体状态中的虚拟文件系统，用于上下文卸载：
- 文件操作：`ls()`、`read_file()`、`write_file()`、`edit_file()`
- 通过信息持久化进行上下文管理
- 在对话轮次间启用智能体"记忆"
- 通过在文件中存储详细信息减少令牌使用

### `3_subagents.ipynb` - 上下文隔离
掌握子智能体委托以处理复杂工作流：
- 创建具有专注工具集的专业化子智能体
- 上下文隔离以防止混乱和任务干扰
- `task()` 委托工具和智能体注册模式
- 独立研究流的并行执行能力

### `4_full_agent.ipynb` - 完整研究智能体
将所有技术结合成一个生产就绪的研究智能体：
- TODO、文件和子智能体的集成
- 具有智能上下文卸载的真实网络搜索
- 内容摘要和战略思考工具
- 与 LangGraph Studio 集成的复杂研究任务完整工作流

每个笔记本都基于前面的概念构建，最终形成一个能够处理现实世界研究和分析任务的复杂智能体架构。