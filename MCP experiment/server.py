#!/usr/bin/env python3
"""
Minimal MCP server that exposes:
  - get_weather(city: str) -> str
  - read_file(path: str)   -> str
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
import httpx

# --------------------------- Tools ---------------------------------

async def get_weather(city: str) -> str:
    return "Worked"

async def read_file(path: str) -> str:
    """Return the first 4 kB of a local file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read(4096)

# --------------------------- MCP plumbing --------------------------

app = Server("demo_mcp")

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> str:
    """Dispatcher for every tool that the client may invoke."""
    if name == "get_weather":
        return await get_weather(arguments["city"])
    if name == "read_file":
        return await read_file(arguments["path"])
    raise ValueError(f"Unknown tool {name!r}")

@app.list_tools()
async def handle_list_tools():
    """Return JSON schema for each tool."""
    return [
        {
            "name": "get_weather",
            "description": "Current weather for a city",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        },
        {
            "name": "read_file",
            "description": "Read a local file",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    ]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())