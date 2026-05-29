# Step 4 — Multi-Server Agent (Sentiment + Browser)

This agent connects to **two MCP servers simultaneously**:
1. Your local Gradio sentiment server
2. Playwright browser automation (fetches and clicks web pages)

## Prerequisites

1. Step 2 sentiment server must be running
2. Playwright MCP server (auto-installed by npx on first run)

## Run

```bash
pip install "huggingface_hub[mcp]>=0.32.0"
tiny-agents run multi-agent.json
```

## Try These Prompts

```
Go to https://example.com, read the first paragraph, and analyze its sentiment.
```

```
Search the web for "AI agents 2026" and tell me the sentiment of the first result's title.
```

```
What is the sentiment of the content at https://huggingface.co/blog ?
```

## Why This Is Powerful

The LLM brain decides on its own which tool to call:
- Needs to browse a URL? → calls Playwright's `navigate` tool
- Needs sentiment analysis? → calls your Gradio `sentiment_analysis` tool
- Needs both? → calls them in sequence

You wrote **zero glue code**. MCP handles the routing.

## Composability Diagram

```
User prompt
    ↓
LLM (Qwen 2.5)
    ├── browse_url(url)         → Playwright MCP server
    ├── screenshot()           → Playwright MCP server
    └── sentiment_analysis(t)  → Your Gradio MCP server
```
