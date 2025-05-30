"""Enhanced weather tool with OpenMeteo API integration."""

import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from ..config import config
from ..models import WeatherReport, ToolResponse

logger = logging.getLogger(__name__)

# OpenMeteo API endpoints
OPENMETEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPENMETEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_enhanced(city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves detailed weather information using OpenMeteo API (completely free).
    
    Args:
        city (str): The name of the city
        country_code (str, optional): ISO 3166 country code (e.g., 'US', 'GB')
    
    Returns:
        Dict[str, Any]: Structured weather information or error details
    """
    try:
        # Step 1: Get coordinates for the city using OpenMeteo Geocoding
        location_query = f"{city},{country_code}" if country_code else city
        
        geocoding_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        logger.info(f"Fetching coordinates for {city}")
        geo_response = requests.get(OPENMETEO_GEOCODING_URL, params=geocoding_params, timeout=10)
        
        if geo_response.status_code != 200:
            logger.error(f"Geocoding failed with status {geo_response.status_code}")
            return _get_mock_weather(city)
        
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return ToolResponse(
                status="error",
                message=f"City '{city}' not found. Please check the spelling or try with a country code.",
                error_code="CITY_NOT_FOUND"
            ).dict()
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "Unknown")
        
        # Step 2: Get weather data using coordinates
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m", 
                "wind_speed_10m",
                "weather_code",
                "surface_pressure"
            ],
            "timezone": "auto",
            "units": "metric"
        }
        
        logger.info(f"Fetching weather for {city_name} at {latitude}, {longitude}")
        weather_response = requests.get(OPENMETEO_WEATHER_URL, params=weather_params, timeout=10)
        
        if weather_response.status_code != 200:
            logger.error(f"Weather API failed with status {weather_response.status_code}")
            return _get_mock_weather(city)
        
        weather_data = weather_response.json()
        current = weather_data["current"]
        
        # Convert weather code to description
        weather_description = _get_weather_description(current.get("weather_code", 0))
        
        weather_report = WeatherReport(
            city=city_name,
            country=country,
            temperature_celsius=round(current.get("temperature_2m", 0), 1),
            temperature_fahrenheit=round(current.get("temperature_2m", 0) * 9/5 + 32, 1),
            description=weather_description,
            humidity=current.get("relative_humidity_2m"),
            wind_speed=current.get("wind_speed_10m"),
            pressure=current.get("surface_pressure"),
            visibility=None,  # Not available in OpenMeteo
            timestamp=datetime.now()
        )
        
        return ToolResponse(
            status="success",
            data=weather_report.dict(),
            message=f"Weather information retrieved for {weather_report.city}, {weather_report.country} (OpenMeteo API)"
        ).dict()
        
    except requests.RequestException as e:
        logger.error(f"OpenMeteo API request failed: {e}")
        return _get_mock_weather(city)
    except Exception as e:
        logger.error(f"Unexpected error in get_weather_enhanced: {e}")
        return ToolResponse(
            status="error",
            message="An unexpected error occurred while fetching weather data",
            error_code="UNEXPECTED_ERROR"
        ).dict()

def get_weather_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast using OpenMeteo API.
    
    Args:
        city (str): The name of the city
        days (int): Number of days for forecast (1-14)
    
    Returns:
        Dict[str, Any]: Weather forecast data or error details
    """
    try:
        days = min(max(days, 1), 14)  # OpenMeteo supports up to 14 days
        
        # Step 1: Get coordinates for the city
        geocoding_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geo_response = requests.get(OPENMETEO_GEOCODING_URL, params=geocoding_params, timeout=10)
        
        if geo_response.status_code != 200:
            return _get_mock_forecast(city, days)
        
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return ToolResponse(
                status="error",
                message=f"City '{city}' not found for forecast",
                error_code="CITY_NOT_FOUND"
            ).dict()
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "Unknown")
        
        # Step 2: Get forecast data
        forecast_params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min", 
                "weather_code",
                "relative_humidity_2m_mean",
                "wind_speed_10m_max"
            ],
            "timezone": "auto",
            "forecast_days": days,
            "units": "metric"
        }
        
        forecast_response = requests.get(OPENMETEO_WEATHER_URL, params=forecast_params, timeout=10)
        
        if forecast_response.status_code != 200:
            return _get_mock_forecast(city, days)
        
        forecast_data = forecast_response.json()
        daily = forecast_data["daily"]
        
        forecasts = []
        for i in range(len(daily["time"])):
            temp_max = daily["temperature_2m_max"][i]
            temp_min = daily["temperature_2m_min"][i]
            avg_temp = (temp_max + temp_min) / 2
            
            forecasts.append({
                "date": daily["time"][i],
                "temperature_celsius": round(avg_temp, 1),
                "temperature_fahrenheit": round(avg_temp * 9/5 + 32, 1),
                "temperature_max": round(temp_max, 1),
                "temperature_min": round(temp_min, 1),
                "description": _get_weather_description(daily["weather_code"][i]),
                "humidity": daily["relative_humidity_2m_mean"][i],
                "wind_speed": daily["wind_speed_10m_max"][i]
            })
        
        return ToolResponse(
            status="success",
            data={
                "city": city_name,
                "country": country,
                "forecast_days": forecasts
            },
            message=f"{days}-day weather forecast for {city_name} (OpenMeteo API)"
        ).dict()
        
    except Exception as e:
        logger.error(f"Error in get_weather_forecast: {e}")
        return _get_mock_forecast(city, days)

def _get_weather_description(weather_code: int) -> str:
    """
    Convert OpenMeteo weather code to human-readable description.
    
    Args:
        weather_code (int): Weather code from OpenMeteo
    
    Returns:
        str: Human-readable weather description
    """
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy", 
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    return weather_codes.get(weather_code, f"Unknown weather (code: {weather_code})")

def _get_mock_weather(city: str) -> Dict[str, Any]:
    """Fallback mock weather data when API is unavailable."""
    mock_data = {
        "new york": {"temp": 22, "desc": "Partly Cloudy", "country": "US"},
        "london": {"temp": 15, "desc": "Rainy", "country": "GB"},
        "tokyo": {"temp": 28, "desc": "Sunny", "country": "JP"},
        "paris": {"temp": 18, "desc": "Cloudy", "country": "FR"},
        "sydney": {"temp": 25, "desc": "Clear", "country": "AU"}
    }
    
    city_lower = city.lower()
    if city_lower in mock_data:
        data = mock_data[city_lower]
        weather_report = WeatherReport(
            city=city.title(),
            country=data["country"],
            temperature_celsius=data["temp"],
            temperature_fahrenheit=data["temp"] * 9/5 + 32,
            description=data["desc"],
            humidity=65,
            wind_speed=5.2,
            pressure=1013.25,
            visibility=10.0,
            timestamp=datetime.now()
        )
        
        return ToolResponse(
            status="success",
            data=weather_report.dict(),
            message=f"Mock weather data for {city} (API unavailable)"
        ).dict()
    else:
        return ToolResponse(
            status="error",
            message=f"Weather information for '{city}' is not available in mock data",
            error_code="MOCK_CITY_NOT_FOUND"
        ).dict()

def _get_mock_forecast(city: str, days: int) -> Dict[str, Any]:
    """Fallback mock forecast data."""
    from datetime import timedelta
    
    base_temp = 20
    forecasts = []
    base_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    
    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        
        forecasts.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "temperature_celsius": base_temp + i,
            "temperature_fahrenheit": (base_temp + i) * 9/5 + 32,
            "description": ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Clear"][i % 5],
            "humidity": 60 + i * 5,
            "wind_speed": 3.0 + i * 0.5
        })
    
    return ToolResponse(
        status="success",
        data={
            "city": city.title(),
            "country": "Unknown",
            "forecasts": forecasts
        },
        message=f"Mock {days}-day forecast for {city} (API unavailable)"
    ).dict()
