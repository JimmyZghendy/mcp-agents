# Workshop Concepts — AI Agents & MCP Servers
### For students: what to understand and why each step matters

---

## What is MCP?

MCP (Model Context Protocol) is an open standard created by Anthropic. It defines a common language for connecting AI models to external tools, data sources, and capabilities.

Think of it like USB-C for AI: instead of every AI app inventing its own plugin system, MCP is the standard connector. Any MCP-compatible agent can use any MCP-compatible server — without custom glue code.

**The three MCP primitives:**

| Primitive | Who controls it | Side effects? | Use for |
|-----------|----------------|---------------|---------|
| **Tool** | The model | Yes (can write, send, call APIs) | Actions the agent takes |
| **Resource** | The client/app | No (read-only) | Data the agent reads |
| **Prompt** | The user | No | Reusable prompt templates |

---

## Step 1 vs Step 2 — Two ways to build an MCP server

### Step 1: FastMCP (code-first)

You write a Python function and decorate it with `@mcp.tool()`, `@mcp.resource()`, or `@mcp.prompt()`. FastMCP wraps it into a proper MCP server automatically.

```python
@mcp.tool()
def get_weather(city: str) -> dict:
    return {"city": city, "temperature": 22}
```

This is the **developer path**: full control, any logic you want, runs as a local process.

**Transport: stdio** — the agent spawns the server as a subprocess and communicates via stdin/stdout. Fast, simple, no networking needed.

### Step 2: Gradio (UI-first)

You write a Gradio interface (a UI wrapper around a Python function), then add one flag: `mcp_server=True`. Gradio automatically:
- Creates a web UI at `localhost:7860`
- Exposes a REST API
- Exposes an MCP server at `/gradio_api/mcp/sse`

```python
demo = gr.Interface(fn=analyze, inputs="text", outputs="text")
demo.launch(mcp_server=True)
```

This is the **product path**: you get a demo UI, an API, and an MCP server all at once.

**Transport: HTTP + SSE** — the agent connects to the server over the network as a long-lived HTTP connection. Needed when the server is remote or shared.

### Key difference

| | Step 1 (FastMCP) | Step 2 (Gradio) |
|---|---|---|
| Transport | stdio (local subprocess) | HTTP + SSE (network) |
| Has UI | No | Yes |
| Best for | Internal tools, local agents | Shared tools, demos, APIs |
| Starts automatically | Yes (spawned by agent) | No (must be running first) |

---

## Step 3 — What is an agent, really?

### The agent loop

An agent is not a single API call. It's a loop:

```
Perceive → Reason → Plan → Act → Observe → repeat
```

1. **Perceive**: The agent reads the user's message and the available tools
2. **Reason**: The model decides what to do next
3. **Plan**: It selects a tool and prepares arguments
4. **Act**: It calls the tool via MCP
5. **Observe**: It reads the tool result
6. **Iterate**: It repeats until it has a final answer

### What is tiny-agents?

`tiny-agents` is a minimal agent runtime from HuggingFace. You define the agent in a JSON file:

```json
{
  "model": "gpt-4o-mini",
  "provider": "openai",
  "apiKey": "sk-...",
  "servers": [{ "type": "sse", "url": "http://localhost:7860/gradio_api/mcp/sse" }]
}
```

No Python. No code. The agent connects to the MCP server, discovers tools, and enters the loop automatically.

### Why does Step 3 need Step 2 running?

Because Step 3 uses **HTTP+SSE transport**. The agent connects to `localhost:7860` over the network — if Gradio isn't running, there's nothing to connect to. This is unlike Step 7, which uses **stdio** and spawns the server automatically.

---

## Step 4 — Why two MCP servers?

An agent can be connected to multiple MCP servers simultaneously. Each server exposes its own tools. The model sees all tools from all servers as one unified list.

In Step 4, the agent has:
- **Playwright MCP server** — can open browsers, navigate pages, extract content
- **Sentiment MCP server** (from Step 2) — can analyze sentiment of text

When you ask: *"Go to BBC News and analyze the sentiment of the headlines"*, the agent:
1. Uses Playwright to browse to the URL and extract headlines
2. Uses the sentiment tool to score each headline
3. Combines the results into one answer

**The agent figures out which tool to use for each step on its own.** You didn't tell it "use Playwright first, then sentiment." It reasoned that out from the task description and the tool descriptions.

This is the core value of MCP: tools are composable. You can mix and match servers without rewriting the agent.

---

## Steps 5 & 6 — Optional extensions

### Step 5: smolagents (programmatic agents)

`smolagents` is a Python library (also from HuggingFace) for building agents in code instead of JSON. You get:
- Full control over the agent loop
- Ability to add logic between steps (logging, filtering, retry)
- Code-first configuration

Use this when tiny-agents is too limiting — e.g., you want to save results to a database between tool calls, or run multiple agents in parallel.

### Step 6: MCP Sampling

Sampling is the most advanced MCP primitive. Normally:
- Agent (model) → calls → Tool (server)

With sampling, the direction reverses:
- Tool (server) → asks model to generate text → Agent (model)

Example use case: a document generation tool that asks the model to write a section, then embeds it in a PDF. The server controls the model, not just the other way around.

This is rare in practice but important to understand — MCP is a two-way protocol.

---

## Step 7 — The full agentic pipeline

Step 7 is the crown jewel. It demonstrates everything at once: a real business task, fully autonomous execution, multiple tools chained in sequence, and a formatted output artifact (email report).

### The five tools

| Tool | What it does |
|------|-------------|
| `list_resumes` | Scans the folder for `.txt`, `.pdf`, `.docx` resume files |
| `read_resume` | Reads any file — resumes or the job description |
| `score_candidate` | Scores one resume against a JD using keyword/pattern matching |
| `rank_candidates` | Sorts all scores and produces a ranked table |
| `send_email` | Formats and sends (or prints) the final report |

### How the agent knows what to do

The intelligence is in `PROMPT.md` — the system prompt. It tells the agent:
- The exact sequence of steps to follow
- Never ask the user questions — act autonomously
- Where to find the job description (hardcoded path)
- What thresholds to use (60+ = invite, below 40 = reject)
- What format to use for the email

The model provides **reasoning and orchestration**. The tools provide **execution**. The prompt provides **business rules**.

### What is missing from Step 7 (and what you could add)

This is intentionally left as an exercise. Current limitations:

| Missing feature | What to build |
|----------------|--------------|
| Real email sending | Add SMTP config (Gmail, SendGrid) to `send_email` tool |
| PDF/DOCX parsing | Add `pdfplumber` or `python-docx` to `read_resume` |
| AI-powered scoring | Replace keyword matching with a model call in `score_candidate` |
| Persistent storage | Save scores to a database between runs |
| Web UI | Wrap the agent in a Gradio interface (combine Steps 2 and 7) |
| Scheduling | Run the screener automatically when new resumes are dropped in a folder |

---

## The big picture — what you learned

```
Step 1: MCP primitives (Tool, Resource, Prompt) with FastMCP
Step 2: MCP over HTTP+SSE with Gradio (UI + API + server)
Step 3: Agent loop with tiny-agents (JSON config, no code)
Step 4: Multi-server agents (tool composition)
Step 5: Programmatic agents with smolagents (Python control)
Step 6: MCP Sampling (bidirectional protocol)
Step 7: Full pipeline (autonomous multi-step business task)
```

Each step adds one new idea. By Step 7, you have all the pieces:
- A protocol (MCP) for connecting tools to models
- A server (FastMCP or Gradio) for exposing tools
- A client (tiny-agents or smolagents) for running the agent loop
- A prompt (system prompt) for encoding business rules
- A model (GPT-4o-mini or Claude) for reasoning and orchestration

This is the stack behind most real-world AI agents deployed today.
