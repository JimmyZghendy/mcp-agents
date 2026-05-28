# Step 3 — Connect a Tiny Agent

## Prerequisites

1. Step 2 sentiment server must be running: `cd ../step2-sentiment-server && python app.py`
2. You must be logged in to HF: `huggingface-cli login`

## Install & Run

```bash
pip install -r requirements.txt

# Connect to local server (default)
tiny-agents run agent.json

# Connect to deployed HF Spaces server
# (edit agent_deployed.json first — replace YOUR_USERNAME)
tiny-agents run agent_deployed.json
```

## Try These Prompts

Once the agent is running, type these in the CLI:

```
Analyze the sentiment of: "I can't believe how amazing this workshop is!"
```

```
What is the sentiment of the following sentence: "The weather today is neither good nor bad."
```

```
Analyze this text and tell me if it's positive or negative: 
"The product broke after one day. Customer service was rude. Never buying again."
```

## What's Happening Under the Hood

```
You type a message
    ↓
Tiny Agent sends it to the LLM (Qwen 2.5 72B on Nebius)
    ↓
LLM decides to call the sentiment_analysis MCP tool
    ↓
Agent sends JSON-RPC call to your local Gradio server
    ↓
Gradio runs TextBlob, returns JSON result
    ↓
LLM interprets result and responds in natural language
```

## HF Token Permissions

Your token (from https://huggingface.co/settings/tokens) needs:
- **Inference API** (read) — to call Qwen on Nebius
