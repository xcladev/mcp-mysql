# MCP MySQL

Un servidor MCP (Model Context Protocol) para MySQL basado en el [SDK oficial de MCP](https://github.com/modelcontextprotocol/python-sdk).

## Estado Actual

Este proyecto está en fase inicial, implementando el ejemplo básico del tutorial de MCP. El objetivo es crear un servidor MCP que permita interactuar con bases de datos MySQL de manera segura y estandarizada.

## Requisitos

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (gestor de paquetes Python)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/xcladev/mcp-mysql.git
cd mcp-mysql
```

2. Instala uv (si no lo tienes):

```bash
pipx install uv  # o cargo install uv
```

3. Crea el entorno virtual y sincroniza dependencias:

```bash
uv venv
```

4. ¡Listo! El entorno ya tiene todo lo que necesitas:

```bash
mcp run server.py
```

## Ejemplo Actual

El servidor actual implementa un ejemplo básico con dos funcionalidades:

1. Una herramienta de suma:

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

2. Un recurso de saludo dinámico:

```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

## Próximos Pasos

- [ ] Implementar conexión a MySQL
- [ ] Añadir herramientas para consultas SQL
- [ ] Implementar gestión de transacciones
- [ ] Añadir validación de consultas
- [ ] Implementar manejo de errores

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
