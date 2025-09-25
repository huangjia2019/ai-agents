# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 项目概述

此仓库包含使用 LangGraph 从零开始构建深度智能体的教育材料。它通过一系列 Jupyter 笔记本演示渐进式智能体架构，从基本的 TODO 列表功能开始，进阶到具有文件系统和子智能体生成的完整智能体。

## 开发命令

### 环境设置
```bash
# 使用 uv（首选包管理器）安装依赖项
uv sync

# 运行 Jupyter 笔记本
uv run jupyter notebook

# 替代方案：激活虚拟环境
source .venv/bin/activate
jupyter notebook
```

### 代码质量
```bash
# 使用 ruff 运行代码检查（笔记本和源代码）
uv run ruff check
uv run ruff check notebooks/

# 在可能的情况下自动修复代码检查问题
uv run ruff check --fix
uv run ruff format

# 使用 mypy 运行类型检查
uv run mypy src/

# 安装开发依赖项（包括 ruff 和 mypy）
uv sync --extra dev
```

### LangGraph Studio 集成
```bash
# 启动 LangGraph Studio（如果已安装）
langgraph up

# langgraph.json 文件定义了两个智能体：
# - studio_react_agent: "./src/deep-agents-from-scratch/studio_react_agent.py:agent"
# - react_agent: "./src/deep-agents-from-scratch/react_agent.py:agent"
```

## 架构

### 核心组件

**状态管理 (`state.py`)**
- `DeepAgentState`：使用 todos 和 files 扩展 LangGraph 的 `AgentState`
- `Todo`：用于任务跟踪的 TypedDict，包含状态（待处理/进行中/已完成）
- `file_reducer`：在状态更新中合并文件字典

**虚拟文件系统 (`file_tools.py`)**
- `ls()`：列出存储在智能体状态中的虚拟文件系统中的文件
- `read_file()`：读取文件内容，支持偏移量/限制
- `write_file()`：在虚拟文件系统中创建/覆盖文件
- `edit_file()`：使用精确字符串匹配执行查找和替换编辑

**任务规划 (`todo_tool.py`)**
- `write_todos()`：创建和更新结构化任务列表
- 使用 LangGraph `Command` 类型进行状态更新
- 对上下文管理和长期运行任务至关重要

**智能体实现**
- `react_agent.py`：通过 Tavily 进行互联网搜索的基本 ReAct 智能体
- `studio_react_agent.py`：带有详细文档的 Studio 兼容版本

### 教程进展（笔记本）

1. **1_todo.ipynb**：用于任务规划和进度跟踪的 TODO 列表工具
2. **2_files.ipynb**：虚拟文件系统工具（读取/写入/编辑/列表）
3. **3_subagents.ipynb**：通过子智能体进行任务委托和上下文隔离
4. **4_full_agent.ipynb**：结合所有工具和功能的完整智能体

### 关键模式

**上下文工程技术：**
- 上下文卸载到存储在状态中的虚拟文件
- 用于规划和进度跟踪的 TODO 列表
- 用于上下文隔离的子智能体生成
- 特定任务的提示工程

**状态管理：**
- 所有文件操作都是虚拟的 - 文件仅存在于 LangGraph 状态中
- 通过保存文件系统状态启用回溯/重启
- Todo 列表在智能体交互间持久化

## 环境变量

在项目根目录创建包含所需 API 密钥的 `.env` 文件：
```bash
# 具有外部搜索功能的研究智能体所需
TAVILY_API_KEY=your_tavily_api_key_here

# 模型使用所需
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 可选：用于评估和跟踪
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=deep-agents-from-scratch
```

## 测试

未配置特定的测试框架。通过以下方式测试智能体：
1. 交互式运行笔记本
2. 通过 LangGraph Studio 界面测试
3. 直接执行 Python 脚本

## 重要注意事项

- 虚拟文件系统是临时的 - 仅在智能体执行期间存在
- TODO 工具应限制同时只有一个任务为 in_progress 状态
- 文件编辑操作需要精确的字符串匹配
- 智能体默认使用 Claude Sonnet 4 模型
- `notebooks/utils.py` 中的富格式化工具用于消息显示