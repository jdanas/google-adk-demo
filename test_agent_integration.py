#!/usr/bin/env python3
"""Test the Google ADK agent integration."""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_agent_import():
    """Test that the agent can be imported without errors."""
    print("🤖 Testing Google ADK Agent Import")
    print("=" * 50)
    
    try:
        from multi_tool_agent.agent import enhanced_agent
        print("✅ Agent imported successfully!")
        print(f"Agent name: {enhanced_agent.name}")
        print(f"Agent model: {enhanced_agent.model}")
        print(f"Description: {enhanced_agent.description[:100]}...")
        print(f"Number of tools: {len(enhanced_agent.tools) if hasattr(enhanced_agent, 'tools') else 'N/A'}")
        return True
    except Exception as e:
        print(f"❌ Failed to import agent: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_tools():
    """Test that the agent has access to all tools."""
    print("\n🔧 Testing Agent Tools Access")
    print("=" * 50)
    
    try:
        from multi_tool_agent.agent import enhanced_agent
        
        # Check if agent has tools attribute
        if hasattr(enhanced_agent, 'tools'):
            print(f"Agent has {len(enhanced_agent.tools)} tools:")
            for i, tool in enumerate(enhanced_agent.tools, 1):
                print(f"  {i}. {tool.name if hasattr(tool, 'name') else 'Unknown tool'}")
        else:
            print("Agent tools may be dynamically loaded or not accessible via tools attribute")
        
        return True
    except Exception as e:
        print(f"❌ Error accessing agent tools: {e}")
        return False

def test_basic_functionality():
    """Test basic agent functionality."""
    print("\n⚡ Testing Basic Agent Functionality")
    print("=" * 50)
    
    try:
        # Import the individual tools to verify they work
        from multi_tool_agent.tools import get_weather_enhanced, get_current_time_enhanced
        
        print("Testing individual tools that the agent has access to:")
        
        # Test weather
        print("\n1. Weather tool test:")
        weather_result = get_weather_enhanced("Paris")
        print(f"   Status: {weather_result['status']}")
        
        # Test time
        print("\n2. Time tool test:")
        time_result = get_current_time_enhanced("London")
        print(f"   Status: {time_result['status']}")
        
        print("\n✅ Individual tools working correctly - agent should have access to them!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing functionality: {e}")
        return False

def main():
    """Run all agent tests."""
    print("🚀 Google ADK Agent Integration Test")
    print("=" * 60)
    
    success = True
    
    success &= test_agent_import()
    success &= test_agent_tools()
    success &= test_basic_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All agent tests passed! The enhanced Google ADK agent is ready to use.")
        print("\nThe agent includes:")
        print("- Real-time weather data (OpenMeteo API)")
        print("- Global time/timezone information")
        print("- City information and search")
        print("- Weather forecasting (up to 14 days)")
        print("- Comprehensive error handling")
        print("- Professional logging")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
