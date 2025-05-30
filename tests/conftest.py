"""Test configuration and fixtures."""

import pytest
import os
from unittest.mock import patch
from multi_tool_agent.config import config

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    with patch.object(config, 'WEATHER_API_KEY', 'test_key'):
        with patch.object(config, 'GOOGLE_API_KEY', 'test_key'):
            yield config

@pytest.fixture
def sample_weather_response():
    """Sample weather API response for testing."""
    return {
        "name": "New York",
        "sys": {"country": "US"},
        "main": {
            "temp": 22.5,
            "humidity": 65,
            "pressure": 1013.25
        },
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 3.6},
        "visibility": 10000
    }

@pytest.fixture  
def sample_forecast_response():
    """Sample forecast API response for testing."""
    return {
        "city": {"name": "New York", "country": "US"},
        "list": [
            {
                "dt": 1640995200,  # 2022-01-01 12:00:00 UTC
                "main": {"temp": 20, "humidity": 60},
                "weather": [{"description": "sunny"}],
                "wind": {"speed": 2.5}
            }
        ] * 8  # 8 forecasts to simulate daily data
    }
