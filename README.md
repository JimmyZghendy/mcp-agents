# 🤖 AI Agents Anatomy & MCP Servers — Workshop Code Repo

> **AI Club · Department of Computer Engineering · May 2026**  
> Full working source code for every hands-on step of the workshop.

---

## Prerequisites — Install These First

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.10 | [python.org](https://python.org) |
| Node.js | ≥ 18 | [nodejs.org](https://nodejs.org) |
| npm / npx | comes with Node | — |
| Git | any | [git-scm.com](https://git-scm.com) |

You also need a **Hugging Face account** (free):  
→ [huggingface.co/join](https://huggingface.co/join)

---

## Repo Structure

```
workshop-mcp-agents/
│
├── README.md                   ← You are here
│
├── step1-weather-server/       ← Minimal FastMCP server (tool + resource + prompt)
├── step2-sentiment-server/     ← Gradio MCP server (runs locally + deploy to HF Spaces)
├── step3-tiny-agent/           ← Tiny Agent connecting to your local sentiment server
├── step4-multi-agent/          ← Multi-server agent (sentiment + Playwright browser)
├── step5-smolagents-client/    ← smolagents Python client connecting to MCP server
└── step6-fastmcp-local/        ← Local FastMCP server with MCP Inspector walkthrough
```

---

## Quick Setup (run once)

```bash
# 1. Clone or download this repo, then enter it
cd workshop-mcp-agents

# 2. Log in to Hugging Face CLI (needed for tiny-agents)
pip install huggingface_hub
huggingface-cli login
# → paste your HF token from https://huggingface.co/settings/tokens
#   token needs: inference (read)

# 3. Install npx globally (needed for tiny-agents and mcp-remote)
npm install -g npx
```

---

## Step-by-Step Guide

### Step 1 — Minimal MCP Server (FastMCP)
```bash
cd step1-weather-server
pip install -r requirements.txt
python server.py           # runs the server
# OR inspect it:
mcp dev server.py          # opens http://127.0.0.1:6274
```

### Step 2 — Sentiment Analysis Server (Gradio + MCP)
```bash
cd step2-sentiment-server
pip install -r requirements.txt
python app.py              # web UI at http://localhost:7860
                           # MCP SSE at http://localhost:7860/gradio_api/mcp/sse
```

### Step 3 — Connect a Tiny Agent (Python)
```bash
cd step3-tiny-agent
# Make sure step2 server is running first!
pip install -r requirements.txt
tiny-agents run agent.json
```

### Step 4 — Multi-Server Agent (Sentiment + Browser)
```bash
cd step4-multi-agent
# Make sure step2 server is running first!
tiny-agents run multi-agent.json
```

### Step 5 — smolagents Python Client
```bash
cd step5-smolagents-client
pip install -r requirements.txt
# Make sure step2 server is running first!
python client.py
```

### Step 6 — FastMCP Local with Inspector
```bash
cd step6-fastmcp-local
pip install -r requirements.txt
mcp dev advanced_server.py
# Open http://127.0.0.1:6274, test tools interactively
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `tiny-agents: command not found` | `pip install "huggingface_hub[mcp]>=0.32.0"` |
| `mcp: command not found` | `pip install "mcp[cli]"` |
| `npx: command not found` | `npm install -g npx` |
| HF 401 Unauthorized | Run `huggingface-cli login` again |
| Port 7860 already in use | `kill $(lsof -ti:7860)` then restart |
| TextBlob corpus missing | Run `python -c "import nltk; nltk.download('punkt')"` |

---

## Deploy to Hugging Face Spaces (Optional)

```bash
# From step2-sentiment-server/
git init
git add app.py requirements.txt
git commit -m "MCP sentiment server"
huggingface-cli repo create mcp-sentiment --type space --space-sdk gradio
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-sentiment
git push -u origin main
```

Then update `step3-tiny-agent/agent.json` server URL to your Space URL.
