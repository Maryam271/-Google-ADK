"""
MCP demo — agent that uses an external Airbnb search server.
"""
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

MODEL = "gemini-2.5-pro"

# Configure the Airbnb MCP server (runs locally via npx)
airbnb_mcp = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
        ),
        timeout=30,   # seconds — Airbnb can be slow
    ),
)

root_agent = LlmAgent(
    name="MCPTravel",
    model=MODEL,
    description="Finds Airbnb listings using a real MCP server.",
    instruction=(
        "You are a friendly travel assistant. "
        "Use the Airbnb tools to search listings when the user asks. "
        "Present results as a clean markdown list with name, price, and rating."
    ),
    tools=[airbnb_mcp],
)
