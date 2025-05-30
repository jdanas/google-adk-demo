"""Enhanced Google ADK Agent with comprehensive tools and capabilities."""

import logging
from google.adk.agents import Agent
from .config import config
from .tools import (
    get_weather_enhanced,
    get_weather_forecast,
    get_current_time_enhanced,
    get_timezone_info,
    get_city_info,
    search_cities
)

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Validate configuration
if not config.validate():
    logger.warning("Some configuration keys are missing. Some features may be limited.")

# Enhanced agent with comprehensive capabilities
enhanced_agent = Agent(
    name=config.AGENT_NAME,
    model=config.AGENT_MODEL,
    description=(
        "Advanced multi-tool agent capable of providing detailed weather information, "
        "time data for cities worldwide, location-based services, and city information. "
        "Supports real-time weather data, forecasts, timezone management, and comprehensive "
        "city information including demographics and attractions."
    ),
    instruction=(
        "You are an intelligent and helpful assistant with access to comprehensive tools for "
        "weather, time, and location information. You can:\n\n"
        
        "🌤️ **Weather Services:**\n"
        "- Get current weather for any city worldwide\n"
        "- Provide detailed weather forecasts (up to 5 days)\n"
        "- Include temperature, humidity, wind speed, pressure, and visibility\n\n"
        
        "⏰ **Time Services:**\n"
        "- Get current time for major cities globally\n"
        "- Handle timezone conversions and DST information\n"
        "- Provide UTC offsets and timezone abbreviations\n\n"
        
        "🗺️ **Location Services:**\n"
        "- Provide detailed city information including population and attractions\n"
        "- Search for cities by name, country, or landmarks\n"
        "- List available cities and their details\n\n"
        
        "**Guidelines:**\n"
        "- Always provide helpful and accurate information\n"
        "- If a specific city isn't available, suggest similar alternatives\n"
        "- Include relevant context like temperature in both Celsius and Fahrenheit\n"
        "- Be conversational and friendly in your responses\n"
        "- When errors occur, explain what went wrong and suggest alternatives\n"
        "- For weather forecasts, highlight significant changes or notable conditions\n"
        "- For time queries, include timezone information when relevant"
    ),
    tools=[
        get_weather_enhanced,
        get_weather_forecast,
        get_current_time_enhanced,
        get_timezone_info,
        get_city_info,
        search_cities
    ],
)

# Legacy agent for backward compatibility
root_agent = enhanced_agent

# Export both for flexibility
__all__ = ["enhanced_agent", "root_agent"] 