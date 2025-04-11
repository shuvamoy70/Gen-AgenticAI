"""
Test script for the Network AI Assistant application.
"""
import os
import sys
from app.agents.network_agent import NetworkAgent

def main():
    """
    Test the NetworkAgent class.
    """
    print("Testing NetworkAgent...")
    
    # Initialize the agent
    agent = NetworkAgent(model_name="HuggingFace/distilbert-base-uncased")
    
    # Get model info
    model_info = agent.model_manager.get_model_info()
    print("Model Info:", model_info)
    
    # Test processing a query
    query = "How can I troubleshoot high latency in my network?"
    print(f"Processing query: {query}")
    
    response = agent.process_query(query)
    print("Response:", response)
    
    print("Test completed successfully!")

if __name__ == "__main__":
    main()
