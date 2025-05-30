"""Enhanced weather tool with real API integration."""

import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from ..config import config
from ..models import WeatherReport, ToolResponse

logger = logging.getLogger(__name__)

def get_weather_enhanced(city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves detailed weather information for a specified city using OpenWeatherMap API.
    
    Args:
        city (str): The name of the city
        country_code (str, optional): ISO 3166 country code (e.g., 'US', 'GB')
    
    Returns:
        Dict[str, Any]: Structured weather information or error details
    """
    try:
        # Build location string
        location = f"{city},{country_code}" if country_code else city
        
        # Check if API key is available
        if not config.WEATHER_API_KEY:
            return _get_mock_weather(city)
        
        # Make API request
        url = f"{config.WEATHER_API_BASE_URL}/weather"
        params = {
            "q": location,
            "appid": config.WEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_report = WeatherReport(
                city=data["name"],
                country=data["sys"]["country"],
                temperature_celsius=data["main"]["temp"],
                temperature_fahrenheit=data["main"]["temp"] * 9/5 + 32,
                description=data["weather"][0]["description"].title(),
                humidity=data["main"].get("humidity"),
                wind_speed=data.get("wind", {}).get("speed"),
                pressure=data["main"].get("pressure"),
                visibility=data.get("visibility", 0) / 1000 if data.get("visibility") else None,
                timestamp=datetime.now()
            )
            
            return ToolResponse(
                status="success",
                data=weather_report.dict(),
                message=f"Weather information retrieved for {weather_report.city}, {weather_report.country}"
            ).dict()
            
        elif response.status_code == 404:
            return ToolResponse(
                status="error",
                message=f"City '{city}' not found. Please check the spelling or try with a country code.",
                error_code="CITY_NOT_FOUND"
            ).dict()
        else:
            return ToolResponse(
                status="error",
                message=f"Weather service temporarily unavailable (HTTP {response.status_code})",
                error_code="SERVICE_UNAVAILABLE"
            ).dict()
            
    except requests.RequestException as e:
        logger.error(f"Weather API request failed: {e}")
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
    Get weather forecast for the specified city.
    
    Args:
        city (str): The name of the city
        days (int): Number of days for forecast (1-5)
    
    Returns:
        Dict[str, Any]: Weather forecast data or error details
    """
    try:
        if not config.WEATHER_API_KEY:
            return _get_mock_forecast(city, days)
        
        days = min(max(days, 1), 5)  # Clamp between 1-5
        
        url = f"{config.WEATHER_API_BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": config.WEATHER_API_KEY,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            forecasts = []
            
            for item in data["list"][::8]:  # Take every 8th item (daily forecast)
                forecasts.append({
                    "date": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d"),
                    "temperature_celsius": item["main"]["temp"],
                    "temperature_fahrenheit": item["main"]["temp"] * 9/5 + 32,
                    "description": item["weather"][0]["description"].title(),
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item.get("wind", {}).get("speed", 0)
                })
            
            return ToolResponse(
                status="success",
                data={
                    "city": data["city"]["name"],
                    "country": data["city"]["country"],
                    "forecasts": forecasts
                },
                message=f"{days}-day weather forecast for {data['city']['name']}"
            ).dict()
        else:
            return ToolResponse(
                status="error",
                message=f"Could not retrieve forecast for '{city}'",
                error_code="FORECAST_UNAVAILABLE"
            ).dict()
            
    except Exception as e:
        logger.error(f"Error in get_weather_forecast: {e}")
        return _get_mock_forecast(city, days)

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
