# Gmail 集成工具

将您的电子邮件助手连接到 Gmail 和 Google Calendar API。

## 图

`src/email_assistant/email_assistant_hitl_memory_gmail.py` 图已配置为使用 Gmail 工具。

您只需运行下面的设置即可获得使用您自己的电子邮件运行图所需的凭据。

## 设置凭据

### 1. 设置 Google Cloud 项目并启用所需的 API

#### 启用 Gmail 和 Calendar API

1. 转到 [Google APIs 库并启用 Gmail API](https://developers.google.com/workspace/gmail/api/quickstart/python#enable_the_api)
2. 转到 [Google APIs 库并启用 Google Calendar API](https://developers.google.com/workspace/calendar/api/quickstart/python#enable_the_api)

#### 创建 OAuth 凭据

1. 在[这里](https://developers.google.com/workspace/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)为桌面应用程序授权凭据
2. 转到凭据 → 创建凭据 → OAuth 客户端 ID
3. 将应用程序类型设置为"桌面应用"
4. 点击"创建"

> 注意：如果使用个人电子邮件（非 Google Workspace），请在"受众"下选择"外部"

<img width="1496" alt="Screenshot 2025-04-26 at 7 43 57 AM" src="https://github.com/user-attachments/assets/718da39e-9b10-4a2a-905c-eda87c1c1126" />

> 然后，将自己添加为测试用户

5. 保存下载的 JSON 文件（您在下一步中需要它）

### 2. 设置身份验证文件

1. 将您下载的客户端密钥 JSON 文件移动到 `.secrets` 目录

```bash
# 创建一个密钥目录
mkdir -p src/email_assistant/tools/gmail/.secrets

# 将您下载的客户端密钥移动到密钥目录
mv /path/to/downloaded/client_secret.json src/email_assistant/tools/gmail/.secrets/secrets.json
```

2. 运行 Gmail 设置脚本

```bash
# 运行 Gmail 设置脚本
python src/email_assistant/tools/gmail/setup_gmail.py
```

-  这将打开一个浏览器窗口，供您使用 Google 帐户进行身份验证
-  这将在 `.secrets` 目录中创建一个 `token.json` 文件
-  此令牌将用于 Gmail API 访问

## 与本地部署一起使用

### 1. 使用本地运行的 LangGraph 服务器运行 Gmail 摄取脚本

1. 设置好身份验证后，在本地运行 LangGraph 服务器：

```
langgraph dev
```

2. 在另一个终端中使用所需参数运行摄取脚本：

```bash
python src/email_assistant/tools/gmail/run_ingest.py --email lance@langgraph.dev --minutes-since 1000
```

- 默认情况下，这将使用本地部署 URL (http://127.0.0.1:2024) 并获取过去 1000 分钟的电子邮件。
- 它将使用 LangGraph SDK 将每封电子邮件传递给本地运行的电子邮件助手。
- 它将使用 `email_assistant_hitl_memory_gmail` 图，该图已配置为使用 Gmail 工具。

#### 参数：

- `--graph-name`：要使用的 LangGraph 名称（默认："email_assistant_hitl_memory_gmail"）
- `--email`：要从中获取消息的电子邮件地址（设置 EMAIL_ADDRESS 的替代方案）
- `--minutes-since`：仅处理比此分钟数更新的电子邮件（默认：60）
- `--url`：LangGraph 部署的 URL（默认：http://127.0.0.1:2024）
- `--rerun`：处理已经处理过的电子邮件（默认：false）
- `--early`：处理一封电子邮件后停止（默认：false）
- `--include-read`：包括已经阅读过的电子邮件（默认情况下仅处理未读电子邮件）
- `--skip-filters`：处理所有电子邮件而不进行过滤（默认情况下仅处理您不是发送者的线程中的最新消息）

#### 故障排除：

- **缺少电子邮件？** Gmail API 默认应用过滤器以仅显示重要/主要电子邮件。您可以：
  - 将 `--minutes-since` 参数增加到更大的值（例如，1000）以从更长的时间段获取电子邮件
  - 使用 `--include-read` 标志来处理标记为"已读"的电子邮件（默认情况下仅处理未读电子邮件）
  - 使用 `--skip-filters` 标志来包含所有消息（不仅仅是线程中的最新消息，还包括您发送的消息）
  - 尝试使用所有选项运行以处理所有内容：`--include-read --skip-filters --minutes-since 1000`
  - 使用 `--mock` 标志来使用模拟电子邮件测试系统

### 2. 连接到 Agent Inbox

摄取后，您可以在 Agent Inbox (https://dev.agentinbox.ai/) 中访问所有中断的线程：
* 部署 URL：http://127.0.0.1:2024
* 助手/图 ID：`email_assistant_hitl_memory_gmail`
* 名称：`Graph Name`

## 运行托管部署

### 1. 部署到 LangGraph 平台

1. 导航到 LangSmith 中的部署页面
2. 点击新建部署
3. 将其连接到您的[此仓库](https://github.com/langchain-ai/agents-from-scratch)分支和所需分支
4. 给它一个名称，如 `Yourname-Email-Assistant`
5. 添加以下环境变量：
   * `OPENAI_API_KEY`
   * `GMAIL_SECRET` - 这是 `.secrets/secrets.json` 中的完整字典
   * `GMAIL_TOKEN` - 这是 `.secrets/token.json` 中的完整字典
6. 点击提交
7. 从部署页面获取 `API URL` (https://your-email-assistant-xxx.us.langgraph.app)

### 2. 使用托管部署运行摄取

一旦您的 LangGraph 部署启动并运行，您可以使用以下命令测试电子邮件摄取：

```bash
python src/email_assistant/tools/gmail/run_ingest.py --email lance@langchain.dev --minutes-since 2440 --include-read --url https://your-email-assistant-xxx.us.langgraph.app
```

### 3. 连接到 Agent Inbox

摄取后，您可以在 Agent Inbox (https://dev.agentinbox.ai/) 中访问所有中断的线程：
* 部署 URL：https://your-email-assistant-xxx.us.langgraph.app
* 助手/图 ID：`email_assistant_hitl_memory_gmail`
* 名称：`Graph Name`
* LangSmith API 密钥：`LANGSMITH_API_KEY`

### 4. 设置 Cron 作业

使用托管部署，您可以设置 cron 作业以指定间隔运行摄取脚本。

要自动化电子邮件摄取，请使用包含的设置脚本设置定时 cron 作业：

```bash
python src/email_assistant/tools/gmail/setup_cron.py --email lance@langchain.dev --url https://lance-email-assistant-4681ae9646335abe9f39acebbde8680b.us.langgraph.app
```

#### 参数：

- `--email`：要获取消息的电子邮件地址（必需）
- `--url`：LangGraph 部署 URL（必需）
- `--minutes-since`：仅获取比此分钟数更新的电子邮件（默认：60）
- `--schedule`：Cron 计划表达式（默认："*/10 * * * *" = 每 10 分钟）
- `--graph-name`：要使用的图的名称（默认："email_assistant_hitl_memory_gmail"）
- `--include-read`：包括标记为已读的电子邮件（默认情况下仅处理未读电子邮件）（默认：false）

#### Cron 的工作原理

cron 由两个主要组件组成：

1. **`src/email_assistant/cron.py`**：定义一个简单的 LangGraph 图，它：
   - 调用 `run_ingest.py` 使用的相同 `fetch_and_process_emails` 函数
   - 将其包装在一个简单的图中，以便可以使用 LangGraph 平台作为托管 cron 运行

2. **`src/email_assistant/tools/gmail/setup_cron.py`**：创建定时 cron 作业：
   - 使用 LangGraph SDK `client.crons.create` 为托管的 `cron.py` 图创建 cron 作业

#### 管理 Cron 作业

要查看、更新或删除现有的 cron 作业，您可以使用 LangGraph SDK：

```python
from langgraph_sdk import get_client

# 连接到部署
client = get_client(url="https://your-deployment-url.us.langgraph.app")

# 列出所有 cron 作业
cron_jobs = await client.crons.list()
print(cron_jobs)

# 删除 cron 作业
await client.crons.delete(cron_job_id)
```

## Gmail 摄取的工作原理

Gmail 摄取过程在三个主要阶段中工作：

### 1. CLI 参数 → Gmail 搜索查询

CLI 参数被转换为 Gmail 搜索查询：

- `--minutes-since 1440` → `after:TIMESTAMP`（过去 24 小时的电子邮件）
- `--email you@example.com` → `to:you@example.com OR from:you@example.com`（您是发送者或接收者的电子邮件）
- `--include-read` → 删除 `is:unread` 过滤器（包括已读消息）

例如，运行：
```
python run_ingest.py --email you@example.com --minutes-since 1440 --include-read
```

创建如下 Gmail API 搜索查询：
```
(to:you@example.com OR from:you@example.com) after:1745432245
```

### 2. 搜索结果 → 线程处理

对于搜索返回的每条消息：

1. 脚本获取线程 ID
2. 使用此线程 ID，它获取包含所有消息的**完整线程**
3. 线程中的消息按日期排序以识别最新消息
4. 根据过滤选项，它处理：
   - 在搜索中找到的特定消息（默认行为）
   - 线程中的最新消息（使用 `--skip-filters` 时）

### 3. 默认过滤器和 `--skip-filters` 行为

#### 应用的默认过滤器

在没有 `--skip-filters` 的情况下，系统按顺序应用这三个过滤器：

1. **未读过滤器**（由 `--include-read` 控制）：
   - 默认行为：仅处理未读消息
   - 使用 `--include-read`：处理已读和未读消息
   - 实现：将 `is:unread` 添加到 Gmail 搜索查询
   - 此过滤器在检索任何消息之前在搜索级别发生

2. **发送者过滤器**：
   - 默认行为：跳过您自己的电子邮件地址发送的消息
   - 实现：检查您的电子邮件是否出现在"From"标头中
   - 逻辑：`is_from_user = email_address in from_header`
   - 这防止助手回复您自己的电子邮件

3. **线程位置过滤器**：
   - 默认行为：仅处理每个线程中的最新消息
   - 实现：将消息 ID 与线程中的最后一条消息进行比较
   - 逻辑：`is_latest_in_thread = message["id"] == last_message["id"]`
   - 防止在存在更新回复时处理较旧的消息

这些过滤器的组合意味着只有每个线程中不是由您发送且未读（除非指定 `--include-read`）的最新消息才会被处理。

#### `--skip-filters` 标志的效果

当启用 `--skip-filters` 时：

1. **绕过发送者和线程位置过滤器**：
   - 将处理您发送的消息
   - 将处理不是线程中最新的消息
   - 逻辑：`should_process = skip_filters or (not is_from_user and is_latest_in_thread)`

2. **改变处理哪条消息**：
   - 没有 `--skip-filters`：使用搜索找到的特定消息
   - 使用 `--skip-filters`：始终使用线程中的最新消息
   - 即使最新消息不在搜索结果中找到

3. **未读过滤器仍然适用（除非被覆盖）**：
   - `--skip-filters` 不会绕过未读过滤器
   - 要处理已读消息，您仍必须使用 `--include-read`
   - 这是因为未读过滤器发生在搜索级别

总结：
- 默认：仅处理您不是发送者且是其线程中最新的未读消息
- `--skip-filters`：处理搜索找到的所有消息，使用每个线程中的最新消息
- `--include-read`：在搜索中包含已读消息
- `--include-read --skip-filters`：最全面，处理搜索找到的所有线程中的最新消息

## 重要的 Gmail API 限制

Gmail API 有几个影响电子邮件摄取的限制：

1. **基于搜索的 API**：Gmail 不提供直接的"从时间范围获取所有电子邮件"端点
   - 所有电子邮件检索都依赖于 Gmail 的搜索功能
   - 对于非常新的消息，搜索结果可能会延迟（索引滞后）
   - 搜索结果可能不包括技术上符合条件的所有消息

2. **两阶段检索过程**：
   - 初始搜索以查找相关消息 ID
   - 二次线程检索以获取完整对话
   - 这个两阶段过程是必要的，因为搜索不能保证完整的线程信息