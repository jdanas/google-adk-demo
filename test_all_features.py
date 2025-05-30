#!/usr/bin/env python3
"""Comprehensive test of all agent features."""

import sys
import logging
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from multi_tool_agent.tools import (
    get_weather_enhanced,
    get_weather_forecast,
    get_current_time_enhanced,
    get_timezone_info,
    get_city_info,
    search_cities
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_weather_tools():
    """Test weather functionality."""
    print("🌤️ Testing Weather Tools")
    print("=" * 50)
    
    # Test current weather
    print("\n1. Current Weather for Tokyo:")
    result = get_weather_enhanced("Tokyo")
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            data = result['data']
            print(f"City: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}")
            print(f"Temperature: {data.get('temperature_celsius', 'N/A')}°C / {data.get('temperature_fahrenheit', 'N/A')}°F")
            print(f"Description: {data.get('description', 'N/A')}")
            print(f"Humidity: {data.get('humidity', 'N/A')}%")
            print(f"Wind Speed: {data.get('wind_speed', 'N/A')} m/s")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    # Test weather forecast
    print("\n2. Weather Forecast for London (3 days):")
    result = get_weather_forecast("London", days=3)
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            data = result['data']
            print(f"City: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}")
            print(f"Number of forecast days: {len(data.get('forecast_days', []))}")
            for i, day in enumerate(data.get('forecast_days', [])[:2]):  # Show first 2 days
                print(f"  Day {i+1}: {day.get('temperature_max', 'N/A')}°C max, {day.get('description', 'N/A')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def test_time_tools():
    """Test time functionality."""
    print("\n\n⏰ Testing Time Tools")
    print("=" * 50)
    
    # Test current time
    print("\n1. Current Time in New York:")
    result = get_current_time_enhanced("New York")
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            data = result['data']
            print(f"City: {data.get('city', 'N/A')}")
            print(f"Current Time: {data.get('current_time', 'N/A')}")
            print(f"Timezone: {data.get('timezone', 'N/A')} (UTC{data.get('utc_offset', 'N/A')})")
            print(f"DST Active: {data.get('dst_active', 'N/A')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    # Test timezone info
    print("\n2. Timezone Info for Sydney:")
    result = get_timezone_info("Sydney")
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            data = result['data']
            print(f"City: {data.get('city', 'N/A')}")
            print(f"Timezone: {data.get('timezone_name', 'N/A')}")
            print(f"UTC Offset: {data.get('utc_offset', 'N/A')}")
            print(f"DST Active: {data.get('dst_active', 'N/A')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def test_location_tools():
    """Test location functionality."""
    print("\n\n🗺️ Testing Location Tools")
    print("=" * 50)
    
    # Test city info
    print("\n1. City Info for Paris:")
    result = get_city_info("Paris")
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            data = result['data']
            print(f"City: {data.get('name', 'N/A')}")
            print(f"Country: {data.get('country', 'N/A')}")
            print(f"Population: {data.get('population', 'N/A'):,}")
            print(f"Timezone: {data.get('timezone', 'N/A')}")
            landmarks = data.get('landmarks', [])
            if landmarks:
                print(f"Landmarks: {', '.join(landmarks[:3])}...")  # Show first 3
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    # Test city search
    print("\n2. Search for cities containing 'San':")
    result = search_cities("San")
    print(f"Status: {result['status']}")
    if result['status'] == "success":
        print(f"Message: {result.get('message', 'N/A')}")
        if 'data' in result:
            cities = result['data'].get('cities', [])
            print(f"Found {len(cities)} cities")
            for city in cities[:3]:  # Show first 3
                print(f"  - {city}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def test_error_handling():
    """Test error handling with invalid inputs."""
    print("\n\n🔧 Testing Error Handling")
    print("=" * 50)
    
    # Test with non-existent city
    print("\n1. Weather for non-existent city:")
    result = get_weather_enhanced("NonExistentCity12345")
    print(f"Status: {result['status']}")
    print(f"Message: {result.get('message', 'Unknown error') if result['status'] == 'error' else 'Unexpected success'}")
    
    # Test with invalid timezone
    print("\n2. Time for invalid city:")
    result = get_current_time_enhanced("InvalidCity98765")
    print(f"Status: {result['status']}")
    print(f"Message: {result.get('message', 'Unknown error') if result['status'] == 'error' else 'Unexpected success'}")

def main():
    """Run all tests."""
    print("🚀 Starting Comprehensive Agent Feature Test")
    print("=" * 60)
    
    try:
        test_weather_tools()
        test_time_tools()
        test_location_tools()
        test_error_handling()
        
        print("\n\n✅ All tests completed!")
        print("Check the output above to verify all features are working correctly.")
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
