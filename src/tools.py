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


def describe_table(table: str) -> list[dict]:
    """Returns columns, types, and keys of a table."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                columns = cursor.fetchall()
                return [
                    {
                        "Field": col[0],
                        "Type": col[1],
                        "Null": col[2],
                        "Key": col[3],
                        "Default": col[4],
                        "Extra": col[5],
                    }
                    for col in columns
                ]
    except pymysql.Error as e:
        raise Exception(f"Error describing table: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

describe_table_tool = Tool(
    name="describe_table",
    description="Returns columns, types, and keys of a table.",
    inputSchema={
        "type": "object",
        "properties": {"table": {"type": "string", "description": "Table name"}},
        "required": ["table"]
    },
    function=describe_table
)


def get_foreign_keys(table: str) -> list[dict]:
    """Extracts foreign key relationships for a table."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = (
                    "SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
                    "FROM information_schema.KEY_COLUMN_USAGE "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL"
                )
                cursor.execute(query, (table,))
                fks = cursor.fetchall()
                return [
                    {
                        "column": fk[0],
                        "referenced_table": fk[1],
                        "referenced_column": fk[2],
                    }
                    for fk in fks
                ]
    except pymysql.Error as e:
        raise Exception(f"Error getting foreign keys: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

get_foreign_keys_tool = Tool(
    name="get_foreign_keys",
    description="Extracts foreign key relationships for a table.",
    inputSchema={
        "type": "object",
        "properties": {"table": {"type": "string", "description": "Table name"}},
        "required": ["table"]
    },
    function=get_foreign_keys
)


def get_column_names(table: str) -> list[str]:
    """Returns only the column names of a table."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                columns = cursor.fetchall()
                return [col[0] for col in columns]
    except pymysql.Error as e:
        raise Exception(f"Error getting column names: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

get_column_names_tool = Tool(
    name="get_column_names",
    description="Returns only the column names of a table.",
    inputSchema={
        "type": "object",
        "properties": {"table": {"type": "string", "description": "Table name"}},
        "required": ["table"]
    },
    function=get_column_names
)


def list_app_users(table: str = "users") -> list[dict]:
    """Lists all users from the specified table, excluding password fields."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                columns = [col[0] for col in cursor.fetchall()]
                exclude_fields = {"password", "hashed_password", "passwd"}
                select_fields = [f for f in columns if f.lower() not in exclude_fields]
                query = f"SELECT {', '.join(select_fields)} FROM `{table}`"
                cursor.execute(query)
                users = cursor.fetchall()
                return [dict(zip(select_fields, row)) for row in users]
    except pymysql.Error as e:
        raise Exception(f"Error listing users from table '{table}': {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

list_app_users_tool = Tool(
    name="list_app_users",
    description="Lists all users from the specified table, excluding password fields.",
    inputSchema={
        "type": "object",
        "properties": {
            "table": {"type": "string", "description": "Table name (e.g., users, usuarios)"}
        },
        "required": ["table"]
    },
    function=list_app_users
)


def get_app_user(table: str, field: str, value: str) -> dict | None:
    """Returns a user from the specified table by a unique field, excluding password fields."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                columns = [col[0] for col in cursor.fetchall()]
                exclude_fields = {"password", "hashed_password", "passwd"}
                select_fields = [f for f in columns if f.lower() not in exclude_fields]
                query = f"SELECT {', '.join(select_fields)} FROM `{table}` WHERE `{field}` = %s LIMIT 1"
                cursor.execute(query, (value,))
                row = cursor.fetchone()
                if row:
                    return dict(zip(select_fields, row))
                return None
    except pymysql.Error as e:
        raise Exception(f"Error getting user from table '{table}': {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

get_app_user_tool = Tool(
    name="get_app_user",
    description="Returns a user from the specified table by a unique field, excluding password fields.",
    inputSchema={
        "type": "object",
        "properties": {
            "table": {"type": "string", "description": "Table name (e.g., users, usuarios)"},
            "field": {"type": "string", "description": "Field to search by (e.g., id, username, email)"},
            "value": {"type": "string", "description": "Value to search for"}
        },
        "required": ["table", "field", "value"]
    },
    function=get_app_user
)
