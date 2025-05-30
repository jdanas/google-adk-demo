#!/usr/bin/env python3
"""
Basic usage example for the enhanced Google ADK agent.
This script demonstrates how to interact with the agent for weather and time queries.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from multi_tool_agent.agent import enhanced_agent

def main():
    """Demonstrate basic agent usage."""
    print("🤖 Enhanced Google ADK Agent Demo")
    print("=" * 50)
    
    # Example queries to demonstrate agent capabilities
    example_queries = [
        "What's the weather like in New York?",
        "Can you give me a 3-day weather forecast for London?", 
        "What time is it in Tokyo right now?",
        "Tell me about Paris - what's it famous for?",
        "Search for cities with 'Angeles' in the name",
        "What's the current weather and time in Sydney?"
    ]
    
    print("\n📝 Example Queries:")
    for i, query in enumerate(example_queries, 1):
        print(f"{i}. {query}")
    
    print("\n" + "=" * 50)
    
    # Interactive mode
    print("\n💬 Interactive Mode (type 'quit' to exit)")
    print("Ask me about weather, time, or city information!")
    
    while True:
        try:
            user_input = input("\n🔹 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤔 Thinking...")
            
            # Send query to agent
            response = enhanced_agent.chat(user_input)
            
            print(f"\n🤖 Agent Response:")
            print(f"{response}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different question.")

if __name__ == "__main__":
    main()
