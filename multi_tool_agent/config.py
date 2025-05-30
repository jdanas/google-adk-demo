"""Configuration management for the Google ADK agent."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the agent."""
    
    # API Keys
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Agent Configuration
    AGENT_MODEL: str = os.getenv("AGENT_MODEL", "gemini-2.0-flash")
    AGENT_NAME: str = os.getenv("AGENT_NAME", "enhanced_multi_tool_agent")
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "UTC")
    
    # API Endpoints
    WEATHER_API_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    TIMEZONE_API_BASE_URL: str = "http://worldtimeapi.org/api/timezone"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required_keys = []
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            print(f"Warning: Missing configuration keys: {missing_keys}")
            return False
        return True

config = Config()
