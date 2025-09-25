# LangGraph Studio 使用指南

## 📋 目录

- [概述](#概述)
- [环境准备](#环境准备)
- [LangGraph Studio 启动](#langgraph-studio-启动)
- [Agent 架构设计](#agent-架构设计)
- [测试流程](#测试流程)
- [API 使用指南](#api-使用指南)
- [故障排除](#故障排除)

## 概述

LangGraph Studio 是一个强大的可视化工具，用于构建、测试和调试基于 LangGraph 的 AI Agent。本项目包含了从基础到高级的多个 Agent 实现，展示了不同的 AI 应用模式。

### 核心特性

- **可视化流程图**: 实时查看 Agent 的执行流程
- **交互式测试**: 通过 Web 界面与 Agent 交互
- **实时调试**: 监控每个步骤的输入输出
- **持久化状态**: 支持对话记忆和状态管理
- **人机交互**: 支持人工审核和干预

## 环境准备

### 1. 系统要求

- Python 3.11 或更高版本
- 有效的 OpenAI API 密钥
- 可选的 LangSmith API 密钥（用于追踪）

### 2. 安装依赖

```bash
# 推荐使用 uv（更快更可靠）
pip install uv
uv sync --extra dev

# 或者使用 pip
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT="interrupt-workshop"
```

## LangGraph Studio 启动

### 启动服务

```bash
# 在项目根目录运行
langgraph dev
```

### 访问界面

- **Studio 界面**: http://127.0.0.1:2024
- **API 文档**: http://127.0.0.1:2024/docs

## Agent 架构设计

### 1. langgraph101 - 基础 ReAct Agent

**文件位置**: `src/email_assistant/langgraph_101.py`

**架构设计**:
```
用户输入 → call_llm → 判断是否需要工具？
                    ↓
                需要工具 → run_tool → 结束
                    ↓
                不需要工具 → 直接结束
```

**核心组件**:
- **工具定义**: `write_email` - 模拟邮件发送
- **LLM 节点**: `call_llm` - 分析用户输入并决定工具调用
- **工具执行**: `run_tool` - 执行具体的工具调用
- **路由逻辑**: `should_continue` - 决定下一步执行路径

**适用场景**:
- 学习 LangGraph 基础概念
- 理解 ReAct（Reasoning + Acting）模式
- 简单的工具调用场景

### 2. email_assistant - 基础邮件助手

**文件位置**: `src/email_assistant/email_assistant.py`

**架构设计**:
```
邮件输入 → 邮件分类 → 生成回复 → 发送邮件
    ↓
  紧急/重要 → 立即处理
  普通邮件 → 批量处理
  垃圾邮件 → 过滤
```

**核心功能**:
- **邮件分类**: 根据内容自动分类邮件
- **智能回复**: 基于邮件内容生成合适的回复
- **优先级处理**: 区分紧急和普通邮件

**适用场景**:
- 日常邮件管理
- 自动回复系统
- 邮件分类和优先级排序

### 3. email_assistant_hitl - 人机交互邮件助手

**文件位置**: `src/email_assistant/email_assistant_hitl.py`

**架构设计**:
```
邮件输入 → 分析处理 → 人工审核 → 执行操作
    ↓
  自动处理 → 直接执行
  需要审核 → 等待人工确认
```

**核心功能**:
- **人机协作**: 关键操作需要人工确认
- **审核流程**: 发送邮件前的人工审核
- **灵活控制**: 用户可以选择自动或手动模式

**适用场景**:
- 重要邮件处理
- 需要人工审核的场景
- 提高邮件处理准确性

### 4. email_assistant_hitl_memory - 带记忆的邮件助手

**文件位置**: `src/email_assistant/email_assistant_hitl_memory.py`

**架构设计**:
```
邮件输入 → 记忆检索 → 分析处理 → 人工审核 → 执行操作
    ↓
  学习用户偏好 → 更新记忆 → 改进处理策略
```

**核心功能**:
- **长期记忆**: 使用 LangGraph Store 持久化记忆
- **学习能力**: 从用户反馈中学习偏好
- **个性化**: 根据历史交互调整处理策略

**适用场景**:
- 个性化邮件助手
- 学习用户偏好的系统
- 长期交互的智能助手

### 5. email_assistant_hitl_memory_gmail - Gmail 集成助手

**文件位置**: `src/email_assistant/email_assistant_hitl_memory_gmail.py`

**架构设计**:
```
Gmail API → 邮件获取 → 智能处理 → 人工审核 → Gmail 发送
    ↓
  真实邮件系统 → 完整工作流程
```

**核心功能**:
- **Gmail 集成**: 连接真实的 Gmail 账户
- **完整流程**: 从邮件获取到发送的完整自动化
- **生产就绪**: 可用于实际的邮件管理

**适用场景**:
- 生产环境邮件管理
- 真实 Gmail 账户集成
- 完整的邮件自动化系统

### 6. cron - 定时任务 Agent

**文件位置**: `src/email_assistant/cron.py`

**架构设计**:
```
定时触发 → 任务执行 → 结果处理 → 下次调度
    ↓
  周期性任务 → 自动化处理
```

**核心功能**:
- **定时执行**: 按计划自动执行任务
- **任务调度**: 管理多个定时任务
- **错误处理**: 任务失败时的重试机制

**适用场景**:
- 定期邮件检查
- 自动化报告生成
- 定时数据同步

## 测试流程

### 方法1: Web 界面测试

1. **访问 Studio**: 打开 http://127.0.0.1:2024
2. **选择 Agent**: 从可用 Agent 列表中选择
3. **创建 Thread**: 开始新的对话会话
4. **输入测试消息**: 观察 Agent 的响应和流程图
5. **查看执行过程**: 实时监控每个步骤的执行

### 方法2: API 测试

#### 创建 Thread

```bash
curl -X POST http://127.0.0.1:2024/threads \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"test": "agent_name"}}'
```

#### 运行 Agent

```bash
curl -X POST http://127.0.0.1:2024/threads/{thread_id}/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent_id",
    "input": {
      "messages": [{"role": "user", "content": "你的测试消息"}]
    },
    "stream_mode": ["messages", "debug"]
  }'
```

### 推荐测试顺序

1. **langgraph101** - 理解基础概念
2. **email_assistant** - 体验完整邮件处理流程
3. **email_assistant_hitl** - 体验人机交互功能
4. **email_assistant_hitl_memory** - 了解记忆功能
5. **email_assistant_hitl_memory_gmail** - 真实 Gmail 集成
6. **cron** - 定时任务功能

## API 使用指南

### 可用的 Agent 列表

| Agent ID | 名称 | 功能描述 |
|----------|------|----------|
| e4f5000e-f578-5cdf-becf-9581b5ae5fe1 | langgraph101 | 基础 ReAct Agent |
| 8dc1af3e-739a-5dd0-a8c5-cfd086a25270 | email_assistant | 基础邮件助手 |
| 09f57530-a391-566a-9714-775b041af26e | email_assistant_hitl | 人机交互邮件助手 |
| 354569b8-7efe-512b-a89b-8e37d29faf0d | email_assistant_hitl_memory | 带记忆的邮件助手 |
| 5e2bfab4-4ef3-5729-b1a9-1a92d21b06f5 | email_assistant_hitl_memory_gmail | Gmail 集成助手 |
| 1e8b67f0-e85a-586b-9d00-cb6ebd198c50 | cron | 定时任务 Agent |

### 常用 API 端点

#### 获取所有 Agent

```bash
curl -X POST http://127.0.0.1:2024/assistants/search \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 获取 Agent 详情

```bash
curl http://127.0.0.1:2024/assistants/{assistant_id}
```

#### 获取 Agent 流程图

```bash
curl http://127.0.0.1:2024/assistants/{assistant_id}/graph
```

#### 获取 Thread 状态

```bash
curl http://127.0.0.1:2024/threads/{thread_id}/state
```

### 流式输出模式

支持多种流式输出模式：

- **messages**: 消息流
- **debug**: 调试信息
- **updates**: 状态更新
- **events**: 事件流
- **values**: 值流

## 故障排除

### 常见问题

#### 1. API 密钥错误

**错误信息**: `openai.AuthenticationError: Error code: 401`

**解决方案**:
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 确保 API 密钥有效且有足够的额度

#### 2. LangSmith 连接失败

**错误信息**: `HTTPError('403 Client Error: Forbidden')`

**解决方案**:
- 检查 `LANGSMITH_API_KEY` 是否正确
- 或者暂时禁用 LangSmith 追踪（设置 `LANGSMITH_TRACING=false`）

#### 3. 端口占用

**错误信息**: `Address already in use`

**解决方案**:
- 检查端口 2024 是否被占用
- 使用 `netstat -tlnp | grep 2024` 查看端口状态
- 杀死占用端口的进程

#### 4. 依赖安装失败

**错误信息**: `ModuleNotFoundError`

**解决方案**:
- 确保在虚拟环境中安装依赖
- 运行 `uv sync --extra dev` 重新安装
- 检查 Python 版本是否为 3.11+

### 调试技巧

1. **查看日志**: 终端会显示详细的执行日志
2. **使用 Debug 模式**: 在 API 调用中启用 `debug` 流模式
3. **检查状态**: 使用 API 查看 Thread 和 Agent 状态
4. **逐步测试**: 从简单的 Agent 开始测试

### 性能优化

1. **并发控制**: 调整 `multitask_strategy` 参数
2. **内存管理**: 定期清理不需要的 Thread
3. **缓存配置**: 合理配置 LLM 缓存策略
4. **资源监控**: 监控 CPU 和内存使用情况

## 总结

LangGraph Studio 提供了一个完整的 Agent 开发和测试环境。通过本指南，你可以：

- 理解不同 Agent 的架构设计
- 掌握测试和调试技巧
- 学会使用 API 进行自动化测试
- 解决常见的技术问题

建议按照推荐的测试顺序逐步体验各个 Agent，从基础概念开始，逐步深入到复杂的生产级应用。



