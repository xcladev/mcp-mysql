from mcp.server.fastmcp import FastMCP
from tools import list_tables_tool

mcp = FastMCP("MySQL MCP Server")


@mcp.tool()
def list_tables() -> list:
    """List all available tables in the MySQL database."""
    return list_tables_tool.function()


if __name__ == "__main__":
    mcp.run()