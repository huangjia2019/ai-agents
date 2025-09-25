# 🧱 从零构建深度研究系统

深度研究已经成为最受欢迎的智能体应用之一。[OpenAI](https://openai.com/index/introducing-deep-research/)、[Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)、[Perplexity](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research) 和 [Google](https://gemini.google/overview/deep-research/?hl=en) 都有深度研究产品，能够使用[各种来源](https://www.anthropic.com/news/research)的上下文生成全面的报告。也有许多[开源](https://huggingface.co/blog/open-deep-research)的[实现](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart)。我们构建了一个[开源深度研究工具](https://github.com/langchain-ai/open_deep_research)，它简单且可配置，允许用户使用自己的模型、搜索工具和 MCP 服务器。在这个仓库中，我们将从零开始构建一个深度研究系统！以下是我们将构建的主要组件图：

![概览](https://github.com/user-attachments/assets/b71727bd-0094-40c4-af5e-87cdb02123b4)

## 🚀 快速开始 

### 前置要求

- **Node.js 和 npx**（notebook 3 中的 MCP 服务器需要）：
```bash
# 安装 Node.js（包含 npx）
# 在 macOS 上使用 Homebrew：
brew install node

# 在 Ubuntu/Debian 上：
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装：
node --version
npx --version
```

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
git clone https://github.com/langchain-ai/deep_research_from_scratch
cd deep_research_from_scratch
```

2. 安装包和依赖项（这会自动创建和管理虚拟环境）：
```bash
uv sync
```

3. 在项目根目录下创建包含您的 API 密钥的 `.env` 文件：
```bash
# 创建 .env 文件
touch .env
```

将您的 API 密钥添加到 `.env` 文件中：
```env
# 使用外部搜索的研究智能体所需
TAVILY_API_KEY=your_tavily_api_key_here

# 模型使用所需
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 可选：用于评估和追踪
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=deep_research_from_scratch
```

4. 使用 uv 运行 notebook 或代码：
```bash
# 直接运行 Jupyter notebook
uv run jupyter notebook

# 或者如果您更喜欢激活虚拟环境
source .venv/bin/activate  # 在 Windows 上：.venv\Scripts\activate
jupyter notebook
```

## 背景 

研究是一个开放性任务；回答用户请求的最佳策略无法提前轻易确定。请求可能需要不同的研究策略和不同深度的搜索。考虑这样的请求。 

[智能体](https://langchain-ai.github.io/langgraph/tutorials/workflows/#agent)非常适合研究，因为它们可以灵活应用不同的策略，使用中间结果来指导它们的探索。开放深度研究使用智能体作为三步过程的一部分来进行研究：

1. **范围界定** – 明确研究范围
2. **研究** – 执行研究
3. **写作** – 生成最终报告

## 📝 组织结构 

这个仓库包含 5 个教程 notebook，从零开始构建一个深度研究系统：

### 📚 教程 Notebook

#### 1. 用户澄清和简报生成 (`notebooks/1_scoping.ipynb`)
**目的**：澄清研究范围并将用户输入转换为结构化研究简报

**核心概念**：
- **用户澄清**：使用结构化输出确定是否需要用户提供额外上下文
- **简报生成**：将对话转换为详细的研究问题
- **LangGraph 命令**：使用命令系统进行流程控制和状态更新
- **结构化输出**：使用 Pydantic 模式进行可靠的决策制定

**实现亮点**：
- 两步工作流：澄清 → 简报生成
- 结构化输出模型（`ClarifyWithUser`，`ResearchQuestion`）防止幻觉
- 基于澄清需求的条件路由
- 日期感知提示用于上下文敏感的研究

**您将学到的内容**：状态管理、结构化输出模式、条件路由

---

#### 2. 使用自定义工具的研究智能体 (`notebooks/2_research_agent.ipynb`)
**目的**：使用外部搜索工具构建迭代研究智能体

**核心概念**：
- **智能体架构**：LLM 决策节点 + 工具执行节点模式
- **顺序工具执行**：可靠的同步工具执行
- **搜索集成**：带内容摘要的 Tavily 搜索
- **工具执行**：带工具调用的 ReAct 风格智能体循环

**实现亮点**：
- 为可靠性和简洁性使用同步工具执行
- 内容摘要以压缩搜索结果
- 带条件路由的迭代研究循环
- 用于全面研究的丰富提示工程

**您将学到的内容**：智能体模式、工具集成、搜索优化、研究工作流设计

---

#### 3. 使用 MCP 的研究智能体 (`notebooks/3_research_agent_mcp.ipynb`)
**目的**：将模型上下文协议（MCP）服务器集成为研究工具

**核心概念**：
- **模型上下文协议**：AI 工具访问的标准化协议
- **MCP 架构**：通过 stdio/HTTP 进行客户端-服务器通信
- **LangChain MCP 适配器**：将 MCP 服务器无缝集成为 LangChain 工具
- **本地 vs 远程 MCP**：理解传输机制

**实现亮点**：
- 用于管理 MCP 服务器的 `MultiServerMCPClient`
- 配置驱动的服务器设置（文件系统示例）
- 工具输出显示的丰富格式
- MCP 协议所需的异步工具执行（无需嵌套事件循环）

**您将学到的内容**：MCP 集成、客户端-服务器架构、基于协议的工具访问

---

#### 4. 研究监督器 (`notebooks/4_research_supervisor.ipynb`)
**目的**：为复杂研究任务进行多智能体协调

**核心概念**：
- **监督器模式**：协调智能体 + 工作智能体
- **并行研究**：使用并行工具调用为独立主题的并发研究智能体
- **研究委托**：用于任务分配的结构化工具
- **上下文隔离**：为不同研究主题分离上下文窗口

**实现亮点**：
- 双节点监督器模式（`supervisor` + `supervisor_tools`）
- 使用 `asyncio.gather()` 进行真正并发的并行研究执行
- 用于委托的结构化工具（`ConductResearch`，`ResearchComplete`）
- 带并行研究指令的增强提示
- 研究聚合模式的全面文档

**您将学到的内容**：多智能体模式、并行处理、研究协调、异步编排

---

#### 5. 完整多智能体研究系统 (`notebooks/5_full_agent.ipynb`)
**目的**：集成所有组件的完整端到端研究系统

**核心概念**：
- **三阶段架构**：范围界定 → 研究 → 写作
- **系统集成**：结合范围界定、多智能体研究和报告生成
- **状态管理**：跨子图的复杂状态流
- **端到端工作流**：从用户输入到最终研究报告

**实现亮点**：
- 具有适当状态转换的完整工作流集成
- 带输出模式的监督器和研究员子图
- 带研究综合的最终报告生成
- 用于澄清的基于线程的对话管理

**您将学到的内容**：系统架构、子图组合、端到端工作流

---

### 🎯 关键学习成果

- **结构化输出**：使用 Pydantic 模式进行可靠的 AI 决策制定
- **异步编排**：战略性使用异步模式进行并行协调 vs 同步简洁性
- **智能体模式**：ReAct 循环、监督器模式、多智能体协调
- **搜索集成**：外部 API、MCP 服务器、内容处理
- **工作流设计**：用于复杂多步过程的 LangGraph 模式
- **状态管理**：跨子图和节点的复杂状态流
- **协议集成**：MCP 服务器和工具生态系统

每个 notebook 都基于前面的概念构建，最终形成一个生产就绪的深度研究系统，能够通过智能范围界定和协调执行处理复杂的多面研究查询。 
