
# 🚀 OpenAI Agent SDK

> **A lightweight, extensible SDK for building agentic applications with OpenAI models — tools, planners, and orchestrators included.**

---

## ⚡ Quickstart

```bash
# clone
git clone https://github.com/your-org/openai-agent-sdk.git
cd openai-agent-sdk

# create venv
python -m venv .venv
source .venv/bin/activate

# install
pip install -e .
```

.env (example):

```
OPENAI_API_KEY=sk-...
AGENT_SDK_ENV=development
```

Run the example agent:

```bash
python examples/todo_agent.py
```

---

## 🧠 Core Concepts

- **Agent** — orchestrator that makes decisions, plans tasks, and calls tools.
- **Tool** — a small function or connector (HTTP, DB, shell) that performs an action.
- **Planner** — (optional) module that decomposes goals into steps for the agent.
- **Memory** — short/long-term storage used across steps (Redis, local file, or ephemeral).
- **ModelAdapter** — adapter layer abstracting calls to LLM providers.

---

## 🧪 Examples

### 1) Hello world agent

```python
from agent_sdk import Agent, Tool, OpenAIAdapter

openai = OpenAIAdapter(api_key=os.getenv('OPENAI_API_KEY'))

def echo_tool(payload):
    return {"echo": payload}

tools = {"echo": Tool(fn=echo_tool, description="Returns payload")}
agent = Agent(model=openai, tools=tools)

resp = agent.run("Echo: Hello world")
print(resp)
```

### 2) Planner + Executor

```python
from agent_sdk import PlannerAgent, WebSearchTool, ShellTool

planner_agent = PlannerAgent(model=openai)
planner_agent.register_tool(WebSearchTool())
planner_agent.register_tool(ShellTool())

result = planner_agent.solve("Find the average price of Model X laptop and run a disk check on /dev/sda")
print(result)
```

---

## 🏗 Architecture

```mermaid
flowchart LR
  User[User Input] --> Planner[Planner (LLM)]
  Planner -->|Plan (steps)| Agent[Agent Executor]
  Agent --> ToolRegistry[Tool Registry]
  ToolRegistry --> HTTPTool[HTTP]
  ToolRegistry --> ShellTool[Shell]
  ToolRegistry --> DBTool[Database]
  Agent --> Memory[(Memory Store)]
  Agent --> Logger[Observability]
```

> The Planner creates a step-by-step plan which the Agent executes. Tools are small, testable connectors that the Agent calls.

---

## 🛠 Development

### Project layout

```
openai-agent-sdk/
├─ agent_sdk/
│  ├─ agents/           # Agent implementations (BaseAgent, PlannerAgent)
│  ├─ tools/            # Built-in tools and connectors
│  ├─ adapters/         # Model adapters (OpenAIAdapter, MockAdapter)
│  ├─ memory/           # Memory stores
│  ├─ utils/            # Helpers: logging, tracing
│  └─ __init__.py
├─ examples/
├─ tests/
└─ pyproject.toml
```

### Run tests

```bash
pytest -q
```

### Lint & format

```bash
ruff . && black .
```

---

## ✅ Best Practices

- Keep tools single-responsibility and idempotent where possible.
- Use `MockAdapter` in tests to avoid external API calls.
- Rate-limit tool calls when calling external services.
- Add schema validation for tool inputs/outputs.

---

## 🤝 Contributing

We ❤️ contributions! Please open issues for feature requests and bug reports. See `CONTRIBUTING.md` for the developer workflow.

---

## 📜 Changelog

See `CHANGELOG.md` for release notes and breaking changes.

---

## 📦 License

MIT © Your Org

---

## 📸 Next steps (I can do these for you)

1. Generate the `assets/README-hero.svg` file and push it to the repo.
2. Create a short animated demo GIF (`assets/demo.gif`) showing `examples/todo_agent.py` running.
3. Add CI and coverage badges (I can provide markup and links to GitHub Actions & Coveralls).

Reply with which steps you'd like me to perform and I will update the canvas accordingly.
