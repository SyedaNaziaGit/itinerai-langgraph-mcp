import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")
client = MultiServerMCPClient({
    "aviationstack":{
        "transport":"stdio",
        "command": r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\aviationstack-mcp\.venv\Scripts\python.exe",
        "args": [
                "-m",
                "aviationstack_mcp",
                "mcp",
                "run"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY
            }
    }
})

async def main():
    tools = await client.get_tools()
    print("Available Aviation Tools are:\n")
    for tool in tools:
        print(tool.name)
    
if __name__ == "__main__":
    asyncio.run(main())
'''
Output:
Available Aviation Tools are:

flights_with_airline
historical_flights_by_date
flight_arrival_departure_schedule
future_flights_arrival_departure_schedule
random_aircraft_type
random_airplanes_detailed_info
random_countries_detailed_info
random_cities_detailed_info
list_airports
list_airlines
list_routes
list_taxes
'''
