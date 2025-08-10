🚀 OpenAI Agent SDK
A lightweight, extensible SDK for building agentic applications with OpenAI models — tools, planners, and orchestrators included.

✨ Visual improvements included in this README
Hero SVG (/assets/README-hero.svg) — scalable vector banner that renders perfectly on GitHub and mobile.
Badges for release, license, Python support, and CI status.
Mermaid architecture diagram and code blocks that preserve monospace formatting.
Optional: animated GIF demos (place under /assets/demo.gif).
⚡ Quickstart
# clone
git clone https://github.com/your-org/openai-agent-sdk.git
cd openai-agent-sdk

# create venv
python -m venv .venv
source .venv/bin/activate

# install
pip install -e .
.env (example):

OPENAI_API_KEY=sk-...
AGENT_SDK_ENV=development
Run the example agent:

python examples/todo_agent.py
🧠 Core Concepts
Agent — orchestrator that makes decisions, plans tasks, and calls tools.
Tool — a small function or connector (HTTP, DB, shell) that performs an action.
Planner — (optional) module that decomposes goals into steps for the agent.
Memory — short/long-term storage used across steps (Redis, local file, or ephemeral).
ModelAdapter — adapter layer abstracting calls to LLM providers.
🧪 Examples
1) Hello world agent
from agent_sdk import Agent, Tool, OpenAIAdapter

openai = OpenAIAdapter(api_key=os.getenv('OPENAI_API_KEY'))

def echo_tool(payload):
    return {"echo": payload}

tools = {"echo": Tool(fn=echo_tool, description="Returns payload")}
agent = Agent(model=openai, tools=tools)

resp = agent.run("Echo: Hello world")
print(resp)
2) Planner + Executor
from agent_sdk import PlannerAgent, WebSearchTool, ShellTool

planner_agent = PlannerAgent(model=openai)
planner_agent.register_tool(WebSearchTool())
planner_agent.register_tool(ShellTool())

result = planner_agent.solve("Find the average price of Model X laptop and run a disk check on /dev/sda")
print(result)
🏗 Architecture
Unable to render rich display

Parse error on line 2:
...--> Planner[Planner (LLM)] Planner -->
-----------------------^
Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'

For more information, see https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams

flowchart LR
  User[User Input] --> Planner[Planner (LLM)]
  Planner -->|Plan (steps)| Agent[Agent Executor]
  Agent --> ToolRegistry[Tool Registry]
  ToolRegistry --> HTTPTool[HTTP]
  ToolRegistry --> ShellTool[Shell]
  ToolRegistry --> DBTool[Database]
  Agent --> Memory[(Memory Store)]
  Agent --> Logger[Observability]
The Planner creates a step-by-step plan which the Agent executes. Tools are small, testable connectors that the Agent calls.

🛠 Development
Project layout
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
Run tests
pytest -q
Lint & format
ruff . && black .
✅ Best Practices
Keep tools single-responsibility and idempotent where possible.
Use MockAdapter in tests to avoid external API calls.
Rate-limit tool calls when calling external services.
Add schema validation for tool inputs/outputs.
🤝 Contributing
We ❤️ contributions! Please open issues for feature requests and bug reports. See CONTRIBUTING.md for the developer workflow.

📜 Changelog
See CHANGELOG.md for release notes and breaking changes.

📦 License
MIT © Your Org

📸 Next steps (I can do these for you)
Generate the assets/README-hero.svg file and push it to the repo.
Create a short animated demo GIF (assets/demo.gif) showing examples/todo_agent.py running.
Add CI and coverage badges (I can provide markup and links to GitHub Actions & Coveralls).
Reply with which steps you'd like me to perform and I will update the canvas accordingly.
