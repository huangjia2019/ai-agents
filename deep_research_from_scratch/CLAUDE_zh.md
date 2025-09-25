# 从零构建深度研究系统 - 仓库指南

## 仓库结构

该仓库使用 LangGraph 从零开始构建一个全面的深度研究系统，通过 5 个教程 notebook 逐步演示不同的组件和模式。

```
deep_research_from_scratch/
├── notebooks/              # 交互式教程 notebook（修改这些文件）
│   ├── 1_scoping.ipynb     # 用户澄清和简报生成
│   ├── 2_research_agent.ipynb       # 带自定义工具的研究智能体
│   ├── 3_research_agent_mcp.ipynb   # 带 MCP 服务器的研究智能体
│   ├── 4_research_supervisor.ipynb  # 多智能体监督器协调
│   ├── 5_full_agent.ipynb  # 完整的端到端系统
│   └── utils.py            # notebook 的共享工具
├── src/deep_research_from_scratch/  # 生成的源代码（不要修改）
│   ├── multi_agent_supervisor.py
│   ├── prompts.py
│   ├── research_agent.py
│   ├── research_agent_mcp.py
│   ├── state_*.py
│   └── utils.py
└── README.md              # 全面的文档
```

## 🚨 重要的开发工作流

**`notebooks/` 中的 notebook 是真相来源，应该是唯一修改的文件。**

`src/deep_research_from_scratch/` 中的源代码是使用 `%%writefile` 魔法命令从 notebook 自动生成的。工作原理如下：

### 代码生成的工作原理

1. **Notebook 包含 `%%writefile` 单元格**：每个 notebook 使用 Jupyter 的 `%%writefile` 魔法直接将代码写入 `src/` 中的文件
2. **Notebook 是可执行的教程**：它们交互式地演示概念，同时生成生产代码
3. **源文件是生成的产物**：`src/` 中的 `.py` 文件是输出，不是输入

### 来自 notebook 的示例：
```python
%%writefile ../src/deep_research_from_scratch/research_agent.py

"""
Research Agent Implementation
"""
# ... actual implementation code follows
```

### 开发指南

- ✅ **应该做**：编辑 `notebooks/` 目录中的 notebook
- ✅ **应该做**：运行 notebook 单元格以重新生成源代码
- ✅ **应该做**：通过运行 notebook 来测试更改
- ❌ **不要做**：直接编辑 `src/deep_research_from_scratch/` 中的文件
- ❌ **不要做**：期望对 `src/` 文件的手动更改能够持久化

## 系统架构

该系统实现了一个三阶段的深度研究工作流：

1. **范围界定**（Notebook 1）：澄清研究范围并生成结构化简报
2. **研究**（Notebook 2-4）：使用各种智能体模式执行研究
3. **写作**（Notebook 5）：将研究结果综合成全面报告

### 关键组件

- **范围界定智能体**：澄清用户意图并生成研究简报
- **研究智能体**：使用自定义工具或 MCP 服务器进行迭代研究
- **监督器智能体**：为复杂主题协调多个研究智能体
- **完整系统**：将所有组件集成到端到端工作流中

## 开发快速开始

1. 对 `notebooks/` 中的适当 notebook 进行更改
2. 运行修改的单元格以重新生成源代码
3. 通过运行后续的 notebook 单元格来测试更改
4. `src/` 中生成的代码将自动反映您的更改

这种方法确保交互式教程仍为权威来源，同时自动维护相应的 Python 包结构。

## 代码质量和格式化

### Ruff 格式化检查

为了在生成的源文件中保持一致的代码格式，请定期运行 ruff：

```bash
# 检查格式问题
ruff check src/

# 在可能的情况下自动修复格式问题
ruff check src/ --fix

# 检查特定文件
ruff check src/deep_research_from_scratch/research_agent.py
```

**重要提示**：由于 `src/` 中的源文件是从 notebook 生成的，任何格式问题都应该在 notebook 的 `%%writefile` 单元格中修复，而不是直接在源文件中修复。在 notebook 中修复格式后，通过运行 notebook 单元格来重新生成源文件。

**常见的格式修复需求：**
- **D212**：确保文档字符串摘要从三重引号的同一行开始
- **I001**：正确组织导入（标准库 → 第三方 → 本地导入）
- **F401**：删除未使用的导入
- **D415**：为文档字符串摘要添加句号