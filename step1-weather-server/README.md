# Step 1 — Your First MCP Server

The simplest possible MCP server using FastMCP.

## Run

```bash
pip install -r requirements.txt

# Option A: run directly (stdio transport, no UI)
python server.py

# Option B: run with MCP Inspector (recommended for learning)
mcp dev server.py
# → open http://127.0.0.1:6274
# → click "Connect", try the tools/resources/prompts tabs
```

## What you'll see in the Inspector

- **Tools** → `get_weather` — type a location, click Run, see the response
- **Resources** → `weather://{location}` — browse the resource URI
- **Prompts** → `weather_report` — see the template rendered

## What's in the code

| Primitive | Decorator | Who controls it | Side effects? |
|-----------|-----------|----------------|---------------|
| Tool | `@mcp.tool()` | Model (LLM) | Yes — could call APIs |
| Resource | `@mcp.resource()` | App / Host | No — read-only |
| Prompt | `@mcp.prompt()` | User | No — just text |
