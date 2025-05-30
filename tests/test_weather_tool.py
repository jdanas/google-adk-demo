"""Tests for weather tools."""

import pytest
from unittest.mock import patch, Mock
from multi_tool_agent.tools.weather_tool import get_weather_enhanced, get_weather_forecast

class TestWeatherTool:
    """Test cases for weather functionality."""
    
    def test_get_weather_enhanced_success(self, mock_config, sample_weather_response):
        """Test successful weather retrieval."""
        with patch('multi_tool_agent.tools.weather_tool.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_weather_response
            mock_get.return_value = mock_response
            
            result = get_weather_enhanced("New York")
            
            assert result["status"] == "success"
            assert "data" in result
            assert result["data"]["city"] == "New York"
            assert result["data"]["country"] == "US"
            assert result["data"]["temperature_celsius"] == 22.5
    
    def test_get_weather_enhanced_city_not_found(self, mock_config):
        """Test weather retrieval for non-existent city."""
        with patch('multi_tool_agent.tools.weather_tool.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            result = get_weather_enhanced("NonExistentCity")
            
            assert result["status"] == "error"
            assert result["error_code"] == "CITY_NOT_FOUND"
    
    def test_get_weather_enhanced_mock_fallback(self):
        """Test mock weather data when API is unavailable."""
        with patch('multi_tool_agent.tools.weather_tool.config.WEATHER_API_KEY', None):
            result = get_weather_enhanced("New York")
            
            assert result["status"] == "success"
            assert "Mock weather data" in result["message"]
    
    def test_get_weather_forecast_success(self, mock_config, sample_forecast_response):
        """Test successful weather forecast retrieval."""
        with patch('multi_tool_agent.tools.weather_tool.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_forecast_response
            mock_get.return_value = mock_response
            
            result = get_weather_forecast("New York", 3)
            
            assert result["status"] == "success"
            assert "data" in result
            assert result["data"]["city"] == "New York"
            assert len(result["data"]["forecasts"]) <= 3
