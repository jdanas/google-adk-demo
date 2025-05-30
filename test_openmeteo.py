#!/usr/bin/env python3
"""
Simple test for OpenMeteo weather integration
"""

import requests
import json

def test_openmeteo():
    """Test OpenMeteo API directly"""
    print("🌤️  Testing OpenMeteo API Integration")
    print("=" * 40)
    
    # Test geocoding
    city = "Berlin"
    print(f"🔍 Getting coordinates for {city}...")
    
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        print(f"📍 Geocoding Status: {geo_response.status_code}")
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if geo_data.get("results"):
                location = geo_data["results"][0]
                lat = location["latitude"]
                lon = location["longitude"]
                city_name = location["name"]
                country = location.get("country", "Unknown")
                
                print(f"✅ Found: {city_name}, {country} ({lat}, {lon})")
                
                # Test weather
                print(f"🌡️  Getting weather for {city_name}...")
                
                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m", 
                        "wind_speed_10m",
                        "weather_code"
                    ],
                    "timezone": "auto",
                    "units": "metric"
                }
                
                weather_response = requests.get(weather_url, params=weather_params, timeout=10)
                print(f"🌤️  Weather Status: {weather_response.status_code}")
                
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    current = weather_data["current"]
                    
                    temp = current.get("temperature_2m", 0)
                    humidity = current.get("relative_humidity_2m", 0)
                    wind = current.get("wind_speed_10m", 0)
                    code = current.get("weather_code", 0)
                    
                    print(f"✅ SUCCESS! Weather for {city_name}:")
                    print(f"   🌡️  Temperature: {temp}°C ({temp * 9/5 + 32:.1f}°F)")
                    print(f"   💧 Humidity: {humidity}%")
                    print(f"   💨 Wind Speed: {wind} km/h")
                    print(f"   ☁️  Weather Code: {code}")
                    return True
                else:
                    print(f"❌ Weather API failed: {weather_response.text}")
            else:
                print(f"❌ No results found for {city}")
        else:
            print(f"❌ Geocoding failed: {geo_response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_openmeteo()
    print("\n" + "=" * 40)
    if success:
        print("🎉 OpenMeteo API is working perfectly!")
        print("✅ Your weather tool should now work with any city worldwide")
        print("🆓 Best part: Completely free, no API key needed!")
    else:
        print("❌ OpenMeteo test failed")
        print("💡 Check your internet connection")
