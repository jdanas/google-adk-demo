"""Enhanced time tool with comprehensive timezone support."""

import requests
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, Optional
from ..config import config
from ..models import TimeReport, ToolResponse

logger = logging.getLogger(__name__)

# Comprehensive timezone mapping
TIMEZONE_MAP = {
    # Major cities with their timezone identifiers
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "chicago": "America/Chicago", 
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "rome": "Europe/Rome",
    "madrid": "Europe/Madrid",
    "tokyo": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong",
    "singapore": "Asia/Singapore",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "dubai": "Asia/Dubai",
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "moscow": "Europe/Moscow",
    "istanbul": "Europe/Istanbul",
    "cairo": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "lagos": "Africa/Lagos",
    "toronto": "America/Toronto",
    "vancouver": "America/Vancouver",
    "montreal": "America/Montreal",
    "mexico city": "America/Mexico_City",
    "buenos aires": "America/Argentina/Buenos_Aires",
    "sao paulo": "America/Sao_Paulo",
    "rio de janeiro": "America/Sao_Paulo"
}

def get_current_time_enhanced(city: str) -> Dict[str, Any]:
    """
    Returns comprehensive time information for a specified city.
    
    Args:
        city (str): The name of the city
    
    Returns:
        Dict[str, Any]: Detailed time information or error details
    """
    try:
        city_lower = city.lower().strip()
        
        # First try to get timezone from our mapping
        timezone_id = TIMEZONE_MAP.get(city_lower)
        
        if not timezone_id:
            # Try to find a partial match
            for mapped_city, tz_id in TIMEZONE_MAP.items():
                if city_lower in mapped_city or mapped_city in city_lower:
                    timezone_id = tz_id
                    break
        
        if not timezone_id:
            return ToolResponse(
                status="error",
                message=f"Timezone information for '{city}' is not available. Try major cities like 'New York', 'London', 'Tokyo', etc.",
                error_code="TIMEZONE_NOT_FOUND"
            ).dict()
        
        # Get current time in the timezone
        tz = ZoneInfo(timezone_id)
        now = datetime.now(tz)
        
        # Calculate UTC offset
        utc_offset = now.strftime("%z")
        formatted_offset = f"{utc_offset[:3]}:{utc_offset[3:]}"
        
        time_report = TimeReport(
            city=city.title(),
            timezone=timezone_id,
            current_time=now,
            utc_offset=formatted_offset,
            is_dst=bool(now.dst())
        )
        
        return ToolResponse(
            status="success",
            data=time_report.dict(),
            message=f"Current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        ).dict()
        
    except Exception as e:
        logger.error(f"Error in get_current_time_enhanced: {e}")
        return ToolResponse(
            status="error",
            message="An error occurred while retrieving time information",
            error_code="TIME_ERROR"
        ).dict()

def get_timezone_info(timezone: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific timezone.
    
    Args:
        timezone (str): Timezone identifier (e.g., 'America/New_York')
    
    Returns:
        Dict[str, Any]: Timezone information or error details
    """
    try:
        # Validate timezone
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        
        # Get UTC time for comparison
        utc_now = datetime.now(ZoneInfo("UTC"))
        
        return ToolResponse(
            status="success",
            data={
                "timezone": timezone,
                "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "utc_offset": now.strftime("%z"),
                "is_dst": bool(now.dst()),
                "abbreviation": now.strftime("%Z"),
                "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
            },
            message=f"Timezone information for {timezone}"
        ).dict()
        
    except Exception as e:
        logger.error(f"Error in get_timezone_info: {e}")
        return ToolResponse(
            status="error",
            message=f"Invalid timezone identifier: {timezone}",
            error_code="INVALID_TIMEZONE"
        ).dict()

def list_supported_cities() -> Dict[str, Any]:
    """
    List all cities supported by the time tool.
    
    Returns:
        Dict[str, Any]: List of supported cities grouped by region
    """
    cities_by_region = {
        "North America": [
            "New York", "Los Angeles", "Chicago", "Toronto", "Vancouver", 
            "Montreal", "Mexico City"
        ],
        "Europe": [
            "London", "Paris", "Berlin", "Rome", "Madrid", "Moscow", "Istanbul"
        ],
        "Asia": [
            "Tokyo", "Beijing", "Shanghai", "Hong Kong", "Singapore", 
            "Mumbai", "Delhi", "Dubai"
        ],
        "Oceania": [
            "Sydney", "Melbourne"
        ],
        "Africa": [
            "Cairo", "Johannesburg", "Lagos"
        ],
        "South America": [
            "Buenos Aires", "Sao Paulo", "Rio de Janeiro"
        ]
    }
    
    return ToolResponse(
        status="success",
        data={"supported_cities": cities_by_region},
        message="List of all supported cities for time queries"
    ).dict()
