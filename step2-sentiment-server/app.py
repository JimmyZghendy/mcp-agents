"""
Step 2: Sentiment Analysis MCP Server (Gradio)
================================================
A dual-purpose app:
  - Human UI  : http://localhost:7860
  - MCP server: http://localhost:7860/gradio_api/mcp/sse

The single flag `mcp_server=True` in demo.launch() turns any Gradio
app into a fully compliant MCP server automatically.

Run:
  python app.py

Then test in browser at http://localhost:7860
Or connect a Tiny Agent to http://localhost:7860/gradio_api/mcp/sse
"""

import json
import gradio as gr
from textblob import TextBlob


# ── Core analysis function ────────────────────────────────────────────────────
def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text.

    Args:
        text: The text to analyze (any language supported by TextBlob)

    Returns:
        A JSON string with:
          - polarity    : float from -1.0 (very negative) to 1.0 (very positive)
          - subjectivity: float from 0.0 (very objective) to 1.0 (very subjective)
          - assessment  : "positive" | "neutral" | "negative"
          - confidence  : "high" | "medium" | "low" based on polarity strength
    """
    if not text or not text.strip():
        return json.dumps({"error": "Please provide non-empty text to analyze."})

    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    # Determine sentiment label
    if polarity > 0.1:
        assessment = "positive"
    elif polarity < -0.1:
        assessment = "negative"
    else:
        assessment = "neutral"

    # Determine confidence
    abs_polarity = abs(polarity)
    if abs_polarity > 0.5:
        confidence = "high"
    elif abs_polarity > 0.2:
        confidence = "medium"
    else:
        confidence = "low"

    result = {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "assessment": assessment,
        "confidence": confidence,
        "input_length": len(text),
    }
    return json.dumps(result, indent=2)


# ── Gradio Interface ──────────────────────────────────────────────────────────
demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(
        placeholder="Enter any text to analyze its sentiment...",
        label="Input Text",
        lines=4,
    ),
    outputs=gr.Textbox(
        label="Sentiment Analysis Result (JSON)",
        lines=8,
    ),
    title="🔍 Text Sentiment Analysis",
    description=(
        "Analyze the emotional tone of text. "
        "This app runs as both a human-friendly web UI AND an MCP server. "
        "MCP endpoint: `http://localhost:7860/gradio_api/mcp/sse`"
    ),
    examples=[
        ["I absolutely love this workshop! The content is incredible and so well organized."],
        ["This is a terrible product. I'm completely disappointed and want a refund."],
        ["The meeting was held on Tuesday at 3pm in conference room B."],
        ["I'm not sure how I feel about this. It has some good parts and some bad parts."],
        ["Claude is an AI assistant made by Anthropic."],
    ],
)


# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(
        mcp_server=True,   # ← This one flag makes it an MCP server!
        server_port=7860,
    )
