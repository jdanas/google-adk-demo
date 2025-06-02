#!/usr/bin/env python3
"""
Diagnostic script to test OpenWeatherMap API integration.
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the API key is working."""
    api_key = os.getenv("WEATHER_API_KEY")
    
    print("🔍 OpenWeatherMap API Diagnostics")
    print("=" * 50)
    
    # Check if API key exists
    if not api_key:
        print("❌ ERROR: WEATHER_API_KEY not found in environment variables")
        print("   Please check your .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test API connection
    test_city = "London"
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": test_city,
        "appid": api_key,
        "units": "metric"
    }
    
    print(f"\n🌐 Testing API connection with city: {test_city}")
    print(f"📡 URL: {url}")
    print(f"📋 Params: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Weather data received for {data['name']}, {data['sys']['country']}")
            print(f"🌡️  Temperature: {data['main']['temp']}°C")
            print(f"☁️  Description: {data['weather'][0]['description']}")
            return True
        elif response.status_code == 401:
            print("❌ ERROR: Unauthorized (401)")
            print("   This usually means:")
            print("   - Invalid API key")
            print("   - API key not activated (can take up to 2 hours)")
            print("   - API key exceeded usage limits")
        elif response.status_code == 404:
            print("❌ ERROR: City not found (404)")
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
        
        return False
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timeout")
        print("   Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Connection error")
        print("   Check your internet connection")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unexpected error: {e}")
        return False

def test_agent_integration():
    """Test the agent's weather tool."""
    print("\n🤖 Testing Agent Integration")
    print("-" * 30)
    
    try:
        from multi_tool_agent.tools.weather_tool import get_weather_enhanced
        
        # Test with a city not in mock data
        test_cities = ["Berlin", "Mumbai", "Cairo"]
        
        for city in test_cities:
            print(f"\n📍 Testing {city}:")
            result = get_weather_enhanced(city)
            
            if result["status"] == "success":
                data = result["data"]
                print(f"   ✅ Success: {data['temperature_celsius']}°C, {data['description']}")
                if "Mock weather data" in result["message"]:
                    print("   ⚠️  Note: Using mock data (API might not be working)")
                else:
                    print("   🌐 Real API data!")
            else:
                print(f"   ❌ Failed: {result['message']}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error testing agent: {e}")

def check_config():
    """Check the configuration setup."""
    print("\n⚙️  Configuration Check")
    print("-" * 30)
    
    try:
        from multi_tool_agent.config import config
        
        print(f"Weather API Key: {'Set' if config.WEATHER_API_KEY else 'Not Set'}")
        print(f"API Base URL: {config.WEATHER_API_BASE_URL}")
        print(f"Agent Model: {config.AGENT_MODEL}")
        
        if config.WEATHER_API_KEY:
            print(f"API Key (masked): {config.WEATHER_API_KEY[:8]}...{config.WEATHER_API_KEY[-4:]}")
        
    except Exception as e:
        print(f"❌ Config error: {e}")

def main():
    """Run all diagnostic tests."""
    success = test_api_key()
    check_config()
    test_agent_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 API is working! Your agent should now support real weather data.")
    else:
        print("❌ API test failed. Please check the issues above.")
        print("\n💡 Common solutions:")
        print("   1. Wait 2 hours for new API key activation")
        print("   2. Check API key is correct in .env file")
        print("   3. Verify internet connection")
        print("   4. Check OpenWeatherMap account status")

if __name__ == "__main__":
    main()
