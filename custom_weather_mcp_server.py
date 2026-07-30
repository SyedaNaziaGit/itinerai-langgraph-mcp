import os
import json
import requests

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

#---------------------------------------CREATING CUSTOM MCP TOOL--------------------------------------------
#creating mcp server using fastmcp
mcp = FastMCP("Weather MCP Server")

#creating tool for getting current weather for the city
@mcp.tool
def get_current_weather(city:str):
    url ="https://api.openweathermap.org/data/2.5/weather",
    params={ "q": city,
            "appid": OPEN_WEATHER_MAP_API_KEY,
            "units": "metric"
            }
    response = requests.get( url = url, params = params)
                            
    data = response.json()
    if response.status_code != 200:
        return data
    return {
        "city": data["name"],
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

#creating tool to get the weather forecast for  the city
@mcp.tool()
def get_forecast(city: str):
    url = ("https://api.openweathermap.org/data/2.5/forecast")
    params = {
        "q": city,
        "appid": OPEN_WEATHER_MAP_API_KEY,
        "units": "metric"
    }
    response = requests.get( url = url,params = params)
    data = response.json()
    forecast = []
    # limiting for first 5 forecast entries
    for item in data["list"][:5]:
        forecast.append(
            {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"]
            }
        )
    return { "city": city, "forecast": forecast }

#--------------------------RUN MCP-------------------------
if __name__ == "__main__":
    mcp.run()