import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

#tools available in tavily remote mcp server
async def  main():
    tools = await client.get_tools()
    """
    print("\n MCP Tools Available are: \n")
    for tool in tools:
        print(tool.name)
    """
    #we need tavily search tool only
    search_tool = next(tool for tool in tools if tool.name == "tavily_search")
    result = await search_tool.ainvoke({
        "query":"Best Hotels in Dubai"
    })
    print(result)
    
search_tool = None

#initializing mcp server 
async def initialize_mcp():
    """ Connecting to MCP server and checking tools available"""
    global search_tool
    if search_tool is not None:
        return
    tools = await client.get_tools()
    print("Available MCP Tools:\n")
    for tool in tools:
        print(tool.name)
    #we select a search tool
    search_tool = next(tool for tool in tools if tool=="tavily_search")
        
#tavily mcp server 
async def tavily_mcp_server(query:str):
    await initialize_mcp()  
    result = await search_tool.ainvoke({"query":query})
    return result



if __name__ == "__main__":
    asyncio.run(main())