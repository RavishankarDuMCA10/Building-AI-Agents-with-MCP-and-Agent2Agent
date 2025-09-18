# MCP & Agent2Agent Implementation

## 📌 Overview
This project demonstrates how to build **AI agents** that can communicate using:

- **MCP (Model Context Protocol)** — for exposing server-side tools and prompts.  
- **Agent2Agent (A2A)** — for enabling independent agents to interact and collaborate.  

The implementation includes:
- **Code of Conduct Assistant** (MCP-based agent).  
- **HR Policy Agent** (MCP-powered).  
- **HR Timeoff Agent** (MCP-powered, with datastore).  
- **Router Agent** (built with LangGraph + A2A, routes queries to the correct agent).  

---

## 📂 Project Structure
```
.
├── requirements.txt              # Dependencies
├── code_of_conduct_client.py     # Client for Code of Conduct Agent
├── code_of_conduct_server.py     # MCP Server exposing CoC tools/prompts
├── hr_policy_agent.py            # HR Policy Agent (MCP + LangChain)
├── hr_policy_server.py           # MCP Server for HR Policy
├── hr_timeoff_datastore.py       # Datastore for HR Timeoff balance/requests
├── HR-Timeoff-Agent/             # (implied) MCP server + wrapper for timeoff
├── a2a/                          # Wrappers for A2A servers (router, timeoff, policy)
└── router_hr_agent.py            # Router Agent (LangGraph + A2A)
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the MCP Servers

### 1. Code of Conduct MCP Server
Start server:
```bash
python code_of_conduct_server.py
```

Run client:
```bash
python code_of_conduct_client.py
```

---

### 2. HR Policy MCP Server
Run server:
```bash
python hr_policy_server.py
```

Run agent:
```bash
python hr_policy_agent.py
```

---

### 3. HR Timeoff MCP Server
Run server (streamable HTTP):
```bash
python HR-Timeoff-Agent/hr_timeoff_server.py
```

The server provides tools:
- `get_timeoff_balance`
- `request_timeoff`
- `get_llm_prompt`

---

## 🤝 Agent2Agent (A2A) Setup

### 1. HR Policy Agent A2A Server
Runs on port `9001`.

```bash
python a2a/a2a_wrapper_policy_agent.py
```

### 2. HR Timeoff Agent A2A Server
Runs on port `9002`.

```bash
python a2a/a2a_wrapper_timeoff_agent.py
```

### 3. Router HR Agent
The Router uses **LangGraph** to classify requests:
- `POLICY` → HR Policy Agent  
- `TIMEOFF` → HR Timeoff Agent  
- `UNSUPPORTED` → fallback  

Run:
```bash
python router_hr_agent.py
```

---

## 🧑‍💻 Example Usage

### Query: *“What is the policy on remote work?”*
```
USER : What is the policy on remote work?
AGENT : Remote work is allowed under company HR guidelines...
```

### Query: *“What is my vacation balance?”*
```
USER : What is my vacation balance?
AGENT : You currently have 12 vacation days remaining.
```

### Query: *“File a time off request for 5 days starting from 2025-05-05”*
```
USER : File a time off request for 5 days starting from 2025-05-05
AGENT : The time off request for Alice has been successfully filed.
```

## References
* [GitHub's Reference course](https://github.com/LinkedInLearning/hands-on-ai-building-ai-agents-with-model-context-protocol-mcp-and-agent2agent-a2a-6055298/codespaces)
