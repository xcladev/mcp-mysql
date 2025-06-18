# src/mcp_mysql_server/tools.py

from typing import List
from mcp.types import Tool
from utils.helper import get_db_connection
import pymysql


def list_tables() -> List[str]:
    """List all available tables in the database."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                return tables
    except pymysql.Error as e:
        raise Exception(f"Error listing tables: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


list_tables_tool = Tool(
    name="list_tables",
    description="List all available tables in the MySQL database.",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": []
    },
    function=list_tables
)
