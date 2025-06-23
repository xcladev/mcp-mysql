# MCP MySQL Server

An MCP (Model Context Protocol) server for MySQL that allows secure and standardized interaction with MySQL databases. Based on the [official MCP SDK](https://github.com/modelcontextprotocol/python-sdk).

> **Note:** This MCP server was originally developed to address my own needs and to explore the use of the Model Context Protocol (MCP). However, it is open and freely available for anyone who has similar requirements or wants to experiment with MCP and MySQL integration.

## Features

- ✅ Secure MySQL connection using PyMySQL
- ✅ Database table and schema inspection
- ✅ User table querying (application users, not MySQL system users)
- ✅ Robust error handling and timeouts
- ✅ Environment variable configuration
- ✅ Compatible with standard MCP protocol

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- MySQL server running

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/xcladev/mcp-mysql.git
cd mcp-mysql
```

2. **Install uv (if you don't have it):**

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

3. **Create virtual environment and sync dependencies:**

```bash
uv venv
uv sync
```

4. **Configure environment variables:**
   Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=your_database_name
```

5. **Ready! Run the server:**

```bash
cd src
mcp run server.py
```

## MCP Server Configuration Example

If you want to run the MCP server with a specific configuration (for example, in a `mcp.json` or similar):

```json
{
  "MySQL MCP Server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "C:/xampp/htdocs/Projectes/mcp-mysql",
      "python",
      "src/server.py"
    ],
    "env": {
      "MYSQL_HOST": "localhost",
      "MYSQL_PORT": "3306",
      "MYSQL_USER": "your_user",
      "MYSQL_PASSWORD": "your_password",
      "MYSQL_DATABASE": "your_database"
    }
  }
}
```

Replace the environment variable values with your actual MySQL credentials and database name.

## Available Tools

### `list_tables`

Lists all available tables in the MySQL database.

- **Parameters:** None
- **Returns:** List of table names

### `describe_table`

Returns columns, types, and keys of a table.

- **Parameters:**
  - `table` (string): Table name
- **Returns:** List of column definitions (field, type, nullability, key, default, extra)

### `get_foreign_keys`

Extracts foreign key relationships for a table.

- **Parameters:**
  - `table` (string): Table name
- **Returns:** List of foreign key relationships (column, referenced_table, referenced_column)

### `get_column_names`

Returns only the column names of a table.

- **Parameters:**
  - `table` (string): Table name
- **Returns:** List of column names

### `list_app_users`

Lists all users from the specified application user table (e.g., `users`, `usuarios`), excluding password fields.

- **Parameters:**
  - `table` (string): Table name (e.g., `users`, `usuarios`)
- **Returns:** List of user records (without password fields)

### `get_app_user`

Returns a user from the specified table by a unique field, excluding password fields.

- **Parameters:**
  - `table` (string): Table name (e.g., `users`, `usuarios`)
  - `field` (string): Field to search by (e.g., `id`, `username`, `email`)
  - `value` (string): Value to search for
- **Returns:** User record (without password fields) or `null` if not found

## Project Structure

```
mcp-mysql/
├── src/
│   ├── server.py          # Main MCP server
│   ├── tools.py           # Tool definitions
│   └── utils/
│       └── helper.py      # MySQL connection utilities
├── tests/
│   └── test_tools.py      # Unit tests for tools
├── .env                   # Environment variables (not included in Git)
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Configuration

### Environment Variables

| Variable         | Description       | Default Value |
| ---------------- | ----------------- | ------------- |
| `MYSQL_HOST`     | MySQL server host | `localhost`   |
| `MYSQL_PORT`     | MySQL server port | `3306`        |
| `MYSQL_USER`     | MySQL user        | -             |
| `MYSQL_PASSWORD` | User password     | -             |
| `MYSQL_DATABASE` | Database name     | -             |

### MySQL Configuration

Make sure your MySQL server is properly configured:

1. **MySQL running** on the specified port
2. **User with permissions** to access the database
3. **Existing database** specified in `MYSQL_DATABASE`

## Development

### Adding New Tools

1. **Define the function in `src/tools.py`:**

```python
def new_tool(parameter: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

2. **Create the MCP tool:**

```python
new_tool_tool = Tool(
    name="new_tool",
    description="Tool description.",
    inputSchema={
        "type": "object",
        "properties": {
            "parameter": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["parameter"]
    },
    function=new_tool
)
```

3. **Register the tool in `src/server.py`:**

```python
@mcp.tool()
def new_tool(parameter: str) -> str:
    """Tool description."""
    return new_tool_tool.function(parameter)
```

## Next Steps

- [ ] Add transaction management
- [ ] Implement query validation
- [ ] Add schema management tools
- [ ] Implement query caching
- [ ] Add support for multiple connections

## Troubleshooting

### Connection Error

If you get connection errors, verify:

- Credentials in the `.env` file
- MySQL is running
- User has permissions for the database

### Timeout Error

If queries take too long:

- Check MySQL configuration
- Consider optimizing queries
- Review network configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
