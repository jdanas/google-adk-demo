"""Data models for structured agent responses."""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class WeatherReport(BaseModel):
    """Weather report data model."""
    city: str
    country: str
    temperature_celsius: float
    temperature_fahrenheit: float
    description: str
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    timestamp: datetime

class TimeReport(BaseModel):
    """Time report data model."""
    city: str
    timezone: str
    current_time: datetime
    utc_offset: str
    is_dst: bool

class ToolResponse(BaseModel):
    """Standard response format for all tools."""
    status: str  # "success" or "error"
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
