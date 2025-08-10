#!/usr/bin/env python3
"""
MCP client that uses Ollama (e.g. llama3.1) to decide which tools to call.
"""

import asyncio
import json
from typing import Any, Dict, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ------------- Ollama integration ---------------------------------
import ollama  # pip install ollama

OLLAMA_MODEL = "llama3.2:3b"          # change to whichever tag you pulled
OLLAMA_HOST = "http://localhost:11434"   # or your remote Ollama endpoint
ollama_client = ollama.AsyncClient(host=OLLAMA_HOST)

# ------------------------------------------------------------------


async def main() -> None:
    # 1. Launch the MCP server (same as before)
    server = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Describe the tools to the LLM
            tools_meta = await session.list_tools()
            openai_style_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    },
                }
                for t in tools_meta
            ]

            # 3. Simple chat loop
            messages: List[Dict[str, Any]] = []
            while True:
                user = input("\nUser: ").strip()
                if user.lower() in {"exit", "quit"}:
                    break
                messages.append({"role": "user", "content": user})

                # 4. Ask Ollama
                resp = await ollama_client.chat(
                    model=OLLAMA_MODEL,
                    messages=messages,
                    tools=openai_style_tools,
                )

                assistant_msg = resp["message"]
                messages.append(assistant_msg)

                # 5. Execute any tool calls
                if "tool_calls" in assistant_msg:
                    for tc in assistant_msg["tool_calls"]:
                        name = tc["function"]["name"]
                        args = json.loads(tc["function"]["arguments"])
                        result = await session.call_tool(name, args)

                        # Add the tool result back to history
                        messages.append(
                            {
                                "role": "tool",
                                "content": str(result),
                            }
                        )

                    # 6. Ask Ollama again with the tool results
                    resp2 = await ollama_client.chat(
                        model=OLLAMA_MODEL,
                        messages=messages,
                    )
                    final = resp2["message"]["content"]
                    messages.append({"role": "assistant", "content": final})
                else:
                    final = assistant_msg["content"]

                print("Assistant:", final)


if __name__ == "__main__":
    asyncio.run(main())