"""Location-based tools for city information and search."""

import logging
from typing import Dict, Any, List
from ..models import ToolResponse

logger = logging.getLogger(__name__)

# Database of city information
CITY_DATABASE = {
    "new york": {
        "name": "New York City",
        "country": "United States",
        "state": "New York",
        "population": 8336817,
        "timezone": "America/New_York",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
        "famous_for": ["Statue of Liberty", "Central Park", "Times Square", "Broadway"]
    },
    "london": {
        "name": "London", 
        "country": "United Kingdom",
        "state": "England",
        "population": 9648110,
        "timezone": "Europe/London",
        "coordinates": {"lat": 51.5074, "lon": -0.1278},
        "famous_for": ["Big Ben", "Tower Bridge", "Buckingham Palace", "London Eye"]
    },
    "tokyo": {
        "name": "Tokyo",
        "country": "Japan",
        "state": "Tokyo Metropolis", 
        "population": 14047594,
        "timezone": "Asia/Tokyo",
        "coordinates": {"lat": 35.6762, "lon": 139.6503},
        "famous_for": ["Tokyo Skytree", "Senso-ji Temple", "Shibuya Crossing", "Mount Fuji (nearby)"]
    },
    "paris": {
        "name": "Paris",
        "country": "France",
        "state": "Île-de-France",
        "population": 2161000,
        "timezone": "Europe/Paris",
        "coordinates": {"lat": 48.8566, "lon": 2.3522},
        "famous_for": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe"]
    },
    "sydney": {
        "name": "Sydney",
        "country": "Australia", 
        "state": "New South Wales",
        "population": 5312163,
        "timezone": "Australia/Sydney",
        "coordinates": {"lat": -33.8688, "lon": 151.2093},
        "famous_for": ["Sydney Opera House", "Harbour Bridge", "Bondi Beach", "Royal Botanic Gardens"]
    },
    "dubai": {
        "name": "Dubai",
        "country": "United Arab Emirates",
        "state": "Dubai Emirate",
        "population": 3331420,
        "timezone": "Asia/Dubai", 
        "coordinates": {"lat": 25.2048, "lon": 55.2708},
        "famous_for": ["Burj Khalifa", "Palm Jumeirah", "Dubai Mall", "Burj Al Arab"]
    },
    "singapore": {
        "name": "Singapore",
        "country": "Singapore",
        "state": "Singapore",
        "population": 5685807,
        "timezone": "Asia/Singapore",
        "coordinates": {"lat": 1.3521, "lon": 103.8198},
        "famous_for": ["Marina Bay Sands", "Gardens by the Bay", "Merlion", "Sentosa Island"]
    },
    "los angeles": {
        "name": "Los Angeles",
        "country": "United States",
        "state": "California", 
        "population": 3898747,
        "timezone": "America/Los_Angeles",
        "coordinates": {"lat": 34.0522, "lon": -118.2437},
        "famous_for": ["Hollywood", "Santa Monica Pier", "Griffith Observatory", "Venice Beach"]
    }
}

def get_city_info(city: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a city.
    
    Args:
        city (str): The name of the city
    
    Returns:
        Dict[str, Any]: City information or error details
    """
    try:
        city_lower = city.lower().strip()
        
        # Direct lookup
        if city_lower in CITY_DATABASE:
            city_data = CITY_DATABASE[city_lower].copy()
            return ToolResponse(
                status="success",
                data=city_data,
                message=f"Information retrieved for {city_data['name']}"
            ).dict()
        
        # Partial match lookup
        for db_city, data in CITY_DATABASE.items():
            if city_lower in db_city or db_city in city_lower:
                city_data = data.copy()
                return ToolResponse(
                    status="success", 
                    data=city_data,
                    message=f"Information retrieved for {city_data['name']} (matched '{city}')"
                ).dict()
        
        return ToolResponse(
            status="error",
            message=f"Information for '{city}' is not available. Try cities like New York, London, Tokyo, Paris, etc.",
            error_code="CITY_NOT_FOUND"
        ).dict()
        
    except Exception as e:
        logger.error(f"Error in get_city_info: {e}")
        return ToolResponse(
            status="error",
            message="An error occurred while retrieving city information",
            error_code="CITY_INFO_ERROR"
        ).dict()

def search_cities(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search for cities matching a query.
    
    Args:
        query (str): Search query (city name, country, or keyword)
        limit (int): Maximum number of results to return
    
    Returns:
        Dict[str, Any]: Search results or error details
    """
    try:
        query_lower = query.lower().strip()
        matches = []
        
        for city_key, city_data in CITY_DATABASE.items():
            # Check if query matches city name, country, or famous attractions
            if (query_lower in city_key or
                query_lower in city_data["name"].lower() or
                query_lower in city_data["country"].lower() or
                any(query_lower in attraction.lower() for attraction in city_data["famous_for"])):
                
                matches.append({
                    "name": city_data["name"],
                    "country": city_data["country"], 
                    "population": city_data["population"],
                    "timezone": city_data["timezone"],
                    "famous_for": city_data["famous_for"][:2]  # Show first 2 attractions
                })
        
        # Sort by population (descending) and limit results
        matches.sort(key=lambda x: x["population"], reverse=True)
        matches = matches[:limit]
        
        if matches:
            return ToolResponse(
                status="success",
                data={
                    "query": query,
                    "results": matches,
                    "total_found": len(matches)
                },
                message=f"Found {len(matches)} cities matching '{query}'"
            ).dict()
        else:
            return ToolResponse(
                status="error",
                message=f"No cities found matching '{query}'. Try broader terms or major city names.",
                error_code="NO_RESULTS"
            ).dict()
            
    except Exception as e:
        logger.error(f"Error in search_cities: {e}")
        return ToolResponse(
            status="error",
            message="An error occurred while searching cities",
            error_code="SEARCH_ERROR"
        ).dict()

def list_all_cities() -> Dict[str, Any]:
    """
    List all cities in the database grouped by country.
    
    Returns:
        Dict[str, Any]: All available cities organized by country
    """
    try:
        cities_by_country = {}
        
        for city_data in CITY_DATABASE.values():
            country = city_data["country"]
            if country not in cities_by_country:
                cities_by_country[country] = []
            
            cities_by_country[country].append({
                "name": city_data["name"],
                "state": city_data["state"],
                "population": city_data["population"]
            })
        
        # Sort cities within each country by population
        for country in cities_by_country:
            cities_by_country[country].sort(key=lambda x: x["population"], reverse=True)
        
        return ToolResponse(
            status="success",
            data={
                "cities_by_country": cities_by_country,
                "total_cities": len(CITY_DATABASE)
            },
            message=f"Complete list of {len(CITY_DATABASE)} available cities"
        ).dict()
        
    except Exception as e:
        logger.error(f"Error in list_all_cities: {e}")
        return ToolResponse(
            status="error",
            message="An error occurred while listing cities",
            error_code="LIST_ERROR"
        ).dict()
