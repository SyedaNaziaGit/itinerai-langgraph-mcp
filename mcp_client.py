import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

#-----------------------------------ENV VARS HERE------------------------
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")
OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

#defining LLM
llm = ChatGroq(model = "llama-3.3-70b-versatile")

#creating a mcp client using multiserverclient -using tavily mcp server -remote- using streamable_http transport layer

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport":"streamable_http",
            "url":f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },
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
        },
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

    
search_tool = None
aviation_tools = None
weather_tool = None
forecast_tool = None

#initializing mcp server to get tools necessary
async def initialize_mcp():
    """ Connecting to MCP server and checking tools available"""
    #search tool
    global search_tool
    if search_tool is not None:
        return
    tools = await client.get_tools()
    print("Available MCP Tools:\n")
    for tool in tools:
        print(tool.name)
    #we select a search tool
    search_tool = next(tool for tool in tools if tool=="tavily_search")
    
    #aviation tool
    global aviation_tools
    aviation_tools = { tool.name: tool for tool in tools if tool.name != "tavily_search" }

async def initialize_weather_tools():
    global weather_tool, forecast_tool
    if weather_tool is not None:
        return
    tools = await client.get_tools()
    weather_tool = next( tool for tool in tools if tool.name == "get_current_weather")

    forecast_tool = next(tool for tool in tools if t.name == "get_forecast") 
            
            
            
#tavily mcp server 
async def tavily_mcp_search(query:str):
    await initialize_mcp()  
    result = await search_tool.ainvoke({"query":query})
    return result

#aviation mcp server
async def aviation_mcp_call( tool_name :str,tool_args : dict = None):
    tools = await client.get_tools()
    tool = next(tool  for tool in tools if tool.name == tool_name)
    result = await tool.ainvoke(
        tool_args or {}
    )
    return result

#weather mcp server
async def weather_mcp_search(city: str):
    await initialize_weather_tools()
    return await weather_tool.ainvoke({"city": city})

#forecast mcp server
async def forecast_mcp_search(city: str):
    await initialize_weather_tools()
    return await forecast_tool.ainvoke({"city": city})


#to get airports we use - listairport tool from aviation tools
async def get_airport_list():
    #to  get aviation tool
    await initialize_mcp()
    tool = aviation_tools.get("list_airports")
    if not tool:
        return "Airport tool Unavailable"
    result = await  tool.ainvoke({})
    return result

async def get_airlines_list():
    await initialize_mcp()
    tool = avaiation_tools.get("list_airlines")
    if not tool:
        return "Airline Tool is Unavailable"
    result = await tool.ainvke({})
    return result

#extracting destination
def extract_destination(query: str):
    prompt = f"""
        Extract only the destination city or country.
        Query: {query}
        Return only destination name.
        """
    response = llm.invoke(prompt)
    return response.content.strip()

if __name__ == "__main__":
    asyncio.run(main())