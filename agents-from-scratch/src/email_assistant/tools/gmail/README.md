# Gmail Integration Tools

Connect your email assistant to Gmail and Google Calendar APIs.

## Graph

The `src/email_assistant/email_assistant_hitl_memory_gmail.py` graph is configured to use Gmail tools.
  
You simply need to run the setup below to obtain the credentials needed to run the graph with your own email.

## Setup Credentials

### 1. Set up Google Cloud Project and Enable Required APIs

#### Enable Gmail and Calendar APIs

1. Go to the [Google APIs Library and enable the Gmail API](https://developers.google.com/workspace/gmail/api/quickstart/python#enable_the_api)
2. Go to the [Google APIs Library and enable the Google Calendar API](https://developers.google.com/workspace/calendar/api/quickstart/python#enable_the_api)

#### Create OAuth Credentials

1. Authorize credentials for a desktop application [here](https://developers.google.com/workspace/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)
2. Go to Credentials → Create Credentials → OAuth Client ID
3. Set Application Type to "Desktop app"
4. Click "Create"

> Note: If using a personal email (non-Google Workspace) select "External" under "Audience"

<img width="1496" alt="Screenshot 2025-04-26 at 7 43 57 AM" src="https://github.com/user-attachments/assets/718da39e-9b10-4a2a-905c-eda87c1c1126" />

> Then, add yourself as a test user
 
5. Save the downloaded JSON file (you'll need this in the next step)

### 2. Set Up Authentication Files

1. Move your downloaded client secret JSON file to the `.secrets` directory

```bash
# Create a secrets directory
mkdir -p src/email_assistant/tools/gmail/.secrets

# Move your downloaded client secret to the secrets directory
mv /path/to/downloaded/client_secret.json src/email_assistant/tools/gmail/.secrets/secrets.json
```

2. Run the Gmail setup script

```bash
# Run the Gmail setup script
python src/email_assistant/tools/gmail/setup_gmail.py
```

-  This will open a browser window for you to authenticate with your Google account
-  This will create a `token.json` file in the `.secrets` directory
-  This token will be used for Gmail API access

## Use With A Local Deployment

### 1. Run the Gmail Ingestion Script with Locally Running LangGraph Server

1. Once you have authentication set up, run LangGraph server locally:

```
langgraph dev
```

2. Run the ingestion script in another terminal with desired parameters:

```bash
python src/email_assistant/tools/gmail/run_ingest.py --email lance@langgraph.dev --minutes-since 1000
```

- By default, this will use the local deployment URL (http://127.0.0.1:2024) and fetch emails from the past 1000 minutes.
- It will use the LangGraph SDK to pass each email to the locally running email assistant.
- It will use the `email_assistant_hitl_memory_gmail` graph, which is configured to use Gmail tools.

#### Parameters:

- `--graph-name`: Name of the LangGraph to use (default: "email_assistant_hitl_memory_gmail")
- `--email`: The email address to fetch messages from (alternative to setting EMAIL_ADDRESS)
- `--minutes-since`: Only process emails that are newer than this many minutes (default: 60)
- `--url`: URL of the LangGraph deployment (default: http://127.0.0.1:2024)
- `--rerun`: Process emails that have already been processed (default: false)
- `--early`: Stop after processing one email (default: false)
- `--include-read`: Include emails that have already been read (by default only unread emails are processed)
- `--skip-filters`: Process all emails without filtering (by default only latest messages in threads where you're not the sender are processed)

#### Troubleshooting:

- **Missing emails?** The Gmail API applies filters to show only important/primary emails by default. You can:
  - Increase the `--minutes-since` parameter to a larger value (e.g., 1000) to fetch emails from a longer time period
  - Use the `--include-read` flag to process emails marked as "read" (by default only unread emails are processed)
  - Use the `--skip-filters` flag to include all messages (not just the latest in a thread, and including ones you sent)
  - Try running with all options to process everything: `--include-read --skip-filters --minutes-since 1000`
  - Use the `--mock` flag to test the system with simulated emails

### 2. Connect to Agent Inbox

After ingestion, you can access your all interrupted threads in Agent Inbox (https://dev.agentinbox.ai/):
* Deployment URL: http://127.0.0.1:2024
* Assistant/Graph ID: `email_assistant_hitl_memory_gmail`
* Name: `Graph Name`

## Run A Hosted Deployment

### 1. Deploy to LangGraph Platform

1. Navigate to the deployments page in LangSmith
2. Click New Deployment
3. Connect it to your fork of the [this repo](https://github.com/langchain-ai/agents-from-scratch) and desired branch
4. Give it a name like `Yourname-Email-Assistant`
5. Add the following environment variables:
   * `OPENAI_API_KEY`
   * `GMAIL_SECRET` - This is the full dictionary in `.secrets/secrets.json`
   * `GMAIL_TOKEN` - This is the full dictionary in `.secrets/token.json`
6. Click Submit 
7. Get the `API URL` (https://your-email-assistant-xxx.us.langgraph.app) from the deployment page 

### 2. Run Ingestion with Hosted Deployment

Once your LangGraph deployment is up and running, you can test the email ingestion with:

```bash
python src/email_assistant/tools/gmail/run_ingest.py --email lance@langchain.dev --minutes-since 2440 --include-read --url https://your-email-assistant-xxx.us.langgraph.app
```

### 3. Connect to Agent Inbox

After ingestion, you can access your all interrupted threads in Agent Inbox (https://dev.agentinbox.ai/):
* Deployment URL: https://your-email-assistant-xxx.us.langgraph.app
* Assistant/Graph ID: `email_assistant_hitl_memory_gmail`
* Name: `Graph Name`
* LangSmith API Key: `LANGSMITH_API_KEY`

### 4. Set up Cron Job

With a hosted deployment, you can set up a cron job to run the ingestion script at a specified interval.

To automate email ingestion, set up a scheduled cron job using the included setup script:

```bash
python src/email_assistant/tools/gmail/setup_cron.py --email lance@langchain.dev --url https://lance-email-assistant-4681ae9646335abe9f39acebbde8680b.us.langgraph.app 
```

#### Parameters:

- `--email`: Email address to fetch messages for (required)
- `--url`: LangGraph deployment URL (required)
- `--minutes-since`: Only fetch emails newer than this many minutes (default: 60)
- `--schedule`: Cron schedule expression (default: "*/10 * * * *" = every 10 minutes)
- `--graph-name`: Name of the graph to use (default: "email_assistant_hitl_memory_gmail")
- `--include-read`: Include emails marked as read (by default only unread emails are processed) (default: false)

#### How the Cron Works

The cron consists of two main components:

1. **`src/email_assistant/cron.py`**: Defines a simple LangGraph graph that:
   - Calls the same `fetch_and_process_emails` function used by `run_ingest.py`
   - Wraps this in a simple graph so that it can be run as a hosted cron using LangGraph Platform

2. **`src/email_assistant/tools/gmail/setup_cron.py`**: Creates the scheduled cron job:
   - Uses LangGraph SDK `client.crons.create` to create a cron job for the hosted `cron.py` graph

#### Managing Cron Jobs

To view, update, or delete existing cron jobs, you can use the LangGraph SDK:

```python
from langgraph_sdk import get_client

# Connect to deployment
client = get_client(url="https://your-deployment-url.us.langgraph.app")

# List all cron jobs
cron_jobs = await client.crons.list()
print(cron_jobs)

# Delete a cron job
await client.crons.delete(cron_job_id)
```

## How Gmail Ingestion Works

The Gmail ingestion process works in three main stages:

### 1. CLI Parameters → Gmail Search Query

CLI parameters are translated into a Gmail search query:

- `--minutes-since 1440` → `after:TIMESTAMP` (emails from the last 24 hours)
- `--email you@example.com` → `to:you@example.com OR from:you@example.com` (emails where you're sender or recipient)
- `--include-read` → removes `is:unread` filter (includes read messages)

For example, running:
```
python run_ingest.py --email you@example.com --minutes-since 1440 --include-read
```

Creates a Gmail API search query like:
```
(to:you@example.com OR from:you@example.com) after:1745432245
```

### 2. Search Results → Thread Processing

For each message returned by the search:

1. The script obtains the thread ID
2. Using this thread ID, it fetches the **complete thread** with all messages
3. Messages in the thread are sorted by date to identify the latest message
4. Depending on filtering options, it processes either:
   - The specific message found in the search (default behavior)
   - The latest message in the thread (when using `--skip-filters`)

### 3. Default Filters and `--skip-filters` Behavior

#### Default Filters Applied

Without `--skip-filters`, the system applies these three filters in sequence:

1. **Unread Filter** (controlled by `--include-read`):
   - Default behavior: Only processes unread messages 
   - With `--include-read`: Processes both read and unread messages
   - Implementation: Adds `is:unread` to the Gmail search query
   - This filter happens at the search level before any messages are retrieved

2. **Sender Filter**:
   - Default behavior: Skips messages sent by your own email address
   - Implementation: Checks if your email appears in the "From" header
   - Logic: `is_from_user = email_address in from_header`
   - This prevents the assistant from responding to your own emails

3. **Thread-Position Filter**:
   - Default behavior: Only processes the most recent message in each thread
   - Implementation: Compares message ID with the last message in thread
   - Logic: `is_latest_in_thread = message["id"] == last_message["id"]`
   - Prevents processing older messages when a newer reply exists
   
The combination of these filters means only the latest message in each thread that was not sent by you and is unread (unless `--include-read` is specified) will be processed.

#### Effect of `--skip-filters` Flag

When `--skip-filters` is enabled:

1. **Bypasses Sender and Thread-Position Filters**:
   - Messages sent by you will be processed
   - Messages that aren't the latest in thread will be processed
   - Logic: `should_process = skip_filters or (not is_from_user and is_latest_in_thread)`

2. **Changes Which Message Is Processed**:
   - Without `--skip-filters`: Uses the specific message found by search
   - With `--skip-filters`: Always uses the latest message in the thread
   - Even if the latest message wasn't found in the search results

3. **Unread Filter Still Applies (unless overridden)**:
   - `--skip-filters` does NOT bypass the unread filter
   - To process read messages, you must still use `--include-read`
   - This is because the unread filter happens at the search level

In summary:
- Default: Process only unread messages where you're not the sender and that are the latest in their thread
- `--skip-filters`: Process all messages found by search, using the latest message in each thread
- `--include-read`: Include read messages in the search
- `--include-read --skip-filters`: Most comprehensive, processes the latest message in all threads found by search

## Important Gmail API Limitations

The Gmail API has several limitations that affect email ingestion:

1. **Search-Based API**: Gmail doesn't provide a direct "get all emails from timeframe" endpoint
   - All email retrieval relies on Gmail's search functionality
   - Search results can be delayed for very recent messages (indexing lag)
   - Search results might not include all messages that technically match criteria

2. **Two-Stage Retrieval Process**:
   - Initial search to find relevant message IDs
   - Secondary thread retrieval to get complete conversations
   - This two-stage process is necessary because search doesn't guarantee complete thread information