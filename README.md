# Google ADK Agent Demo

This project demonstrates a multi-tool agent using Google's Agent Development Kit (ADK) with enhanced capabilities for weather, time, and location services.

## Features

- 🌤️ Real-time weather information for multiple cities
- ⏰ Current time for cities worldwide
- 🗺️ Location-based services
- 🔧 Extensible tool architecture
- ✅ Comprehensive testing
- 📊 Structured data validation

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```bash
WEATHER_API_KEY=your_weather_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Usage

```python
from multi_tool_agent.agent import enhanced_agent

# The agent can handle various queries about weather and time
response = enhanced_agent.chat("What's the weather like in London?")
print(response)
```

## Architecture

- `agent.py` - Main agent configuration and tool definitions
- `tools/` - Individual tool implementations
- `models/` - Data models for structured responses
- `config/` - Configuration management
- `tests/` - Test suite

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request
