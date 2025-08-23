from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import asyncio

async def main():
    # Set up the multi-server client
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"],  # Make sure path is correct
                "transport": "stdio"
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",  # Make sure weather server is running here
                "transport": "streamable_http"
            }
        }
    )

    # Fetch tools and set up the agent
    tools = await client.get_tools()
    model = ChatOllama(model="llama3.2:3b")
    agent = create_react_agent(model, tools)

    print("🔁 Chat started! Ask a math or weather question. Type 'exit' to quit.")

    while True:
        user_input = input("🧑 You: ")
        if user_input.strip().lower() == "exit":
            print("👋 Goodbye!")
            break

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )

        # Extract and print the last message from the agent
        final_message = response["messages"][-1].content
        print("🤖 Agent:", final_message)
asyncio.run(main())

