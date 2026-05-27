# Step 2 — Sentiment Analysis MCP Server

## Run Locally

```bash
pip install -r requirements.txt

# Download TextBlob corpora (first time only)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

python app.py
```

- **Web UI**: http://localhost:7860  
- **MCP SSE endpoint**: http://localhost:7860/gradio_api/mcp/sse  
- **API docs**: http://localhost:7860/?view=api  

## Test the MCP Endpoint

Add this to Claude Desktop / Cursor / VS Code MCP config to connect:

```json
{
  "mcpServers": {
    "sentiment": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://localhost:7860/gradio_api/mcp/sse",
        "--transport",
        "sse-only"
      ]
    }
  }
}
```

## Deploy to Hugging Face Spaces

```bash
git init
git add app.py requirements.txt
git commit -m "MCP sentiment server"

# Create space (change YOUR_USERNAME)
huggingface-cli repo create mcp-sentiment --type space --space-sdk gradio

git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-sentiment
git push -u origin main
```

Your live MCP endpoint will be:  
`https://YOUR_USERNAME-mcp-sentiment.hf.space/gradio_api/mcp/sse`

## What the response looks like

```json
{
  "polarity": 0.625,
  "subjectivity": 0.6,
  "assessment": "positive",
  "confidence": "high",
  "input_length": 43
}
```
