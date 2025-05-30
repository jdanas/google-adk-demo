#!/usr/bin/env python3
"""
Advanced usage example showcasing direct tool usage and batch processing.
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from multi_tool_agent.tools import (
    get_weather_enhanced,
    get_weather_forecast,
    get_current_time_enhanced,
    get_city_info,
    search_cities
)

def demo_weather_tools():
    """Demonstrate weather tool capabilities."""
    print("\n🌤️  Weather Tools Demo")
    print("-" * 30)
    
    cities = ["New York", "London", "Tokyo", "Paris"]
    
    for city in cities:
        print(f"\n📍 {city}:")
        
        # Current weather
        weather = get_weather_enhanced(city)
        if weather["status"] == "success":
            data = weather["data"]
            print(f"   🌡️  {data['temperature_celsius']}°C ({data['temperature_fahrenheit']}°F)")
            print(f"   ☁️  {data['description']}")
            print(f"   💧 Humidity: {data['humidity']}%")
        else:
            print(f"   ❌ {weather['message']}")
        
        # 3-day forecast
        forecast = get_weather_forecast(city, 3)
        if forecast["status"] == "success":
            print(f"   📅 3-day forecast:")
            for day in forecast["data"]["forecasts"]:
                print(f"      {day['date']}: {day['temperature_celsius']}°C, {day['description']}")

def demo_time_tools():
    """Demonstrate time tool capabilities."""
    print("\n⏰ Time Tools Demo")
    print("-" * 30)
    
    cities = ["New York", "London", "Tokyo", "Sydney"]
    
    for city in cities:
        time_info = get_current_time_enhanced(city)
        if time_info["status"] == "success":
            data = time_info["data"]
            # Handle datetime object or string
            if isinstance(data["current_time"], str):
                current_time = datetime.fromisoformat(data["current_time"])
            else:
                current_time = data["current_time"]
            print(f"📍 {data['city']}: {current_time.strftime('%H:%M')} ({data['utc_offset']})")
        else:
            print(f"📍 {city}: {time_info['message']}")

def demo_location_tools():
    """Demonstrate location tool capabilities."""
    print("\n🗺️  Location Tools Demo")
    print("-" * 30)
    
    # City information
    cities = ["New York", "Paris", "Tokyo"]
    for city in cities:
        info = get_city_info(city)
        if info["status"] == "success":
            data = info["data"]
            print(f"\n📍 {data['name']}, {data['country']}")
            print(f"   👥 Population: {data['population']:,}")
            print(f"   🏛️  Famous for: {', '.join(data['famous_for'][:2])}")
    
    # City search
    print(f"\n🔍 Searching for cities with 'New':")
    search_result = search_cities("New")
    if search_result["status"] == "success":
        for city in search_result["data"]["results"]:
            print(f"   • {city['name']}, {city['country']} (Pop: {city['population']:,})")

def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n📊 Batch Processing Demo")
    print("-" * 30)
    
    cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
    results = []
    
    for city in cities:
        city_data = {
            "city": city,
            "timestamp": datetime.now().isoformat()
        }
        
        # Get weather
        weather = get_weather_enhanced(city)
        if weather["status"] == "success":
            city_data["weather"] = {
                "temperature_celsius": weather["data"]["temperature_celsius"],
                "description": weather["data"]["description"]
            }
        
        # Get time
        time_info = get_current_time_enhanced(city)
        if time_info["status"] == "success":
            time_data = time_info["data"]["current_time"]
            # Convert datetime object to string if needed
            if hasattr(time_data, 'isoformat'):
                city_data["local_time"] = time_data.isoformat()
            else:
                city_data["local_time"] = time_data
        
        # Get city info
        info = get_city_info(city)
        if info["status"] == "success":
            city_data["population"] = info["data"]["population"]
            city_data["famous_for"] = info["data"]["famous_for"][:2]
        
        results.append(city_data)
    
    # Save results to JSON
    output_file = "city_data_batch.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Batch results saved to {output_file}")
    
    # Display summary
    print(f"\n📈 Summary:")
    for result in results:
        weather_temp = result.get("weather", {}).get("temperature_celsius", "N/A")
        population = result.get("population", "N/A")
        print(f"   {result['city']}: {weather_temp}°C, Pop: {population:,}" if isinstance(population, int) else f"   {result['city']}: {weather_temp}°C, Pop: {population}")

def main():
    """Run all demonstration functions."""
    print("🚀 Advanced Google ADK Agent Tools Demo")
    print("=" * 50)
    
    demo_weather_tools()
    demo_time_tools() 
    demo_location_tools()
    demo_batch_processing()
    
    print(f"\n✅ Demo completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
