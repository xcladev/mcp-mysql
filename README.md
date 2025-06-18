# MCP MySQL Server

An MCP (Model Context Protocol) server for MySQL that allows secure and standardized interaction with MySQL databases. Based on the [official MCP SDK](https://github.com/modelcontextprotocol/python-sdk).

## Features

- ✅ Secure MySQL connection using PyMySQL
- ✅ Database table listing
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
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=your_database_name
```

5. **Ready! Run the server:**

```bash
cd src
mcp run server.py
```

## Available Tools

### `list_tables`

Lists all available tables in the MySQL database.

**Parameters:** None

**Returns:** List of table names

**Usage example:**

```python
# The MCP client can call this tool to get
# all tables from the configured database
```

## Project Structure

```
mcp-mysql/
├── src/
│   ├── server.py          # Main MCP server
│   ├── tools.py           # Tool definitions
│   └── utils/
│       └── helper.py      # MySQL connection utilities
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
