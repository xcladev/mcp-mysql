from mcp.server.fastmcp import FastMCP
from tools import (
    list_tables_tool,
    describe_table_tool,
    get_foreign_keys_tool,
    get_column_names_tool,
    list_app_users_tool,
    get_app_user_tool,
)

mcp = FastMCP("MySQL MCP Server")


@mcp.tool()
def list_tables() -> list:
    """List all available tables in the MySQL database."""
    return list_tables_tool.function()


@mcp.tool()
def describe_table(table: str) -> list:
    """Returns columns, types, and keys of a table."""
    return describe_table_tool.function(table)


@mcp.tool()
def get_foreign_keys(table: str) -> list:
    """Extracts foreign key relationships for a table."""
    return get_foreign_keys_tool.function(table)


@mcp.tool()
def get_column_names(table: str) -> list:
    """Returns only the column names of a table."""
    return get_column_names_tool.function(table)


@mcp.tool()
def list_app_users(table: str) -> list:
    """Lists all users from the specified table, excluding password fields."""
    return list_app_users_tool.function(table)


@mcp.tool()
def get_app_user(table: str, field: str, value: str) -> dict | None:
    """Returns a user from the specified table by a unique field, excluding password fields."""
    return get_app_user_tool.function(table, field, value)


if __name__ == "__main__":
    mcp.run()