import sys
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Weather MCP Server using Open Meteo")
#https://open-meteo.com/en/docs

def _get_lat_long(city: str) -> tuple:
    """Helper function to convert a city name into latitude and longitude coordinates."""
    url = "https://open-meteo.com"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Geocoding service returned status code {response.status_code}")
        
    data = response.json()
    results = data.get("results")
    if not results:
        raise ValueError(f"Could not find coordinates for city: '{city}'")
        
    return results[0]["latitude"], results[0]["longitude"], results[0]["name"]

@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Get the current temperature and windspeed conditions for a given city string."""
    try:
        lat, lon, official_name = _get_lat_long(city)
        
        weather_url = "https://open-meteo.com"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        
        response = requests.get(weather_url, params=weather_params)
        if response.status_code != 200:
            return {"error": f"Weather API returned status code {response.status_code}"}
            
        data = response.json()
        current = data.get("current_weather", {})
        
        return {
            "city": official_name,
            "latitude": lat,
            "longitude": lon,
            "temperature_c": current.get("temperature"),
            "wind_speed_kmh": current.get("windspeed"),
            "weather_code": current.get("weathercode")
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_forecast(city: str) -> dict:
    """Get a 5-day temperature breakdown forecast for a specific city string."""
    try:
        lat, lon, official_name = _get_lat_long(city)
        
        weather_url = "https://open-meteo.com"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto"
        }
        
        response = requests.get(weather_url, params=weather_params)
        if response.status_code != 200:
            return {"error": f"Weather API returned status code {response.status_code}"}
            
        data = response.json()
        daily = data.get("daily", {})
        
        forecast = []
        # Parse the daily lists returned by the API
        dates = daily.get("time", [])[:5]
        max_temps = daily.get("temperature_2m_max", [])[:5]
        min_temps = daily.get("temperature_2m_min", [])[:5]
        
        for i in range(len(dates)):
            forecast.append({
                "date": dates[i],
                "max_temp_c": max_temps[i],
                "min_temp_c": min_temps[i]
            })
            
        return {
            "city": official_name,
            "forecast": forecast
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
