"""
Step 1: Your First MCP Server
==============================
A minimal FastMCP server exposing all 3 primitives:
  - Tool     : get_weather(location) — the AI can call this
  - Resource : weather://{location} — read-only data
  - Prompt   : weather_report(location) — template for the AI

Run:
  python server.py          # starts stdio server
  mcp dev server.py         # starts with MCP Inspector at localhost:6274
"""

from mcp.server.fastmcp import FastMCP

# ── Create the server ────────────────────────────────────────────────────────
mcp = FastMCP("Weather Service")


# ── TOOL: model-controlled, can have side effects ────────────────────────────
@mcp.tool()
def get_weather(location: str) -> str:
    """
    Get the current weather for a specified location.

    Args:
        location: City name or coordinates (e.g. "Beirut", "48.8566,2.3522")

    Returns:
        A string describing current weather conditions.
    """
    # In production you'd call a real weather API here (e.g. OpenWeatherMap)
    return f"Weather in {location}: Sunny, 72°F (22°C), Humidity: 55%"


# ── RESOURCE: app-controlled, read-only, no side effects ─────────────────────
@mcp.resource("weather://{location}")
def weather_resource(location: str) -> str:
    """
    Provide weather data as a structured resource.
    URI pattern: weather://<location>
    """
    return (
        f"Location: {location}\n"
        f"Temperature: 72°F (22°C)\n"
        f"Conditions: Sunny\n"
        f"Humidity: 55%\n"
        f"Wind: 12 km/h NW"
    )


# ── PROMPT: user-controlled, guides the interaction ──────────────────────────
@mcp.prompt()
def weather_report(location: str) -> str:
    """
    Create a structured weather report prompt.

    Args:
        location: The location for the weather report.
    """
    return (
        f"You are a professional meteorologist presenting a weather report. "
        f"Provide a detailed, engaging weather forecast for {location}. "
        f"Include current conditions, what to wear, and any weather advisories."
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # mcp.run() uses stdio transport by default (for local clients)
    # For HTTP+SSE: mcp.run(transport="sse", port=8000)
    mcp.run()
