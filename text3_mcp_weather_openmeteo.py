import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

# Clean system environment context map to keep Windows standard IO pipes safe
system_env = os.environ.copy()

client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "stdio",
            "command": r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\myenv\Scripts\python.exe",
            "args": [
                r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\custom_weather_mcp_server3.py"
            ],
            "env": system_env
        }
    }
)

async def main():
    print("Loading Custom Weather MCP Tools (Open-Meteo Mode)...")
    try:
        tools = await client.get_tools()
        print("\n🎉 Success! Tools loaded successfully:")
        for tool in tools:
            print(f" -> Found Tool: {tool.name}")
    except Exception as e:
        print(f"\n❌ Initialization Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
