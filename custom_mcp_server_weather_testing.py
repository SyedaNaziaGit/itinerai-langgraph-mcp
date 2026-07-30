import os
from dotenv import load_dotenv
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(override=True)

OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

client = MultiServerMCPClient(
    {
        "weather":{
            "transport":"stdio",
            "command": r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\myenv\Scripts\python.exe",
            "args": [ r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\custom_weather_mcp_server.py"
                    ],
            "env": {
                    "OPEN_WEATHER_MAP_API_KEY": OPEN_WEATHER_MAP_API_KEY
                    }
        }
    }
)

async def main():
    print("Loading Custom Weather MCP Tools...")
    tools = await client.get_tools()
    print("Tools loaded!")
    for tool in tools:
        print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())

