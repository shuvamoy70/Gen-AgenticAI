"""
Network AI Assistant - Main Entry Point

This is the main entry point for the Network AI Assistant application.
It initializes the Streamlit app and sets up the agent environment.
"""
import os
import streamlit as st
from app.agents.network_agent import NetworkAgent
from app.utils.logger import setup_logger

# Setup logging
logger = setup_logger()

def main():
    """
    Main function to run the Network AI Assistant application.
    """
    st.set_page_config(
        page_title="Network AI Assistant",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌐 Network AI Assistant")
    st.subheader("An Agentic AI Solution for Network Management")
    
    # Sidebar for configuration
    st.sidebar.title("Configuration")
    model_option = st.sidebar.selectbox(
        "Select AI Model",
        ["HuggingFace/distilbert-base-uncased", "HuggingFace/roberta-base"]
    )
    
    # Initialize the agent
    agent = NetworkAgent(model_name=model_option)
    
    # Main app area
    with st.expander("About this application", expanded=True):
        st.markdown("""
        This application uses agentic AI to help with network management tasks:
        
        - **Network Anomaly Detection**: Identify unusual patterns in network traffic
        - **Predictive Maintenance**: Forecast potential network issues before they occur
        - **Automated Troubleshooting**: Diagnose and suggest solutions for common network problems
        
        The agent uses advanced NLP models from Hugging Face to understand and respond to your requests.
        """)
    
    # User input
    user_input = st.text_area("Describe your network issue or question:", height=100)
    
    if st.button("Submit"):
        if user_input:
            with st.spinner("Agent is processing your request..."):
                # Process the user input through the agent
                response = agent.process_query(user_input)
                
                # Display the response
                st.subheader("Agent Response:")
                st.write(response["answer"])
                
                # Display reasoning if available
                if "reasoning" in response:
                    with st.expander("View Agent Reasoning"):
                        st.write(response["reasoning"])
                
                # Display any recommended actions
                if "actions" in response:
                    st.subheader("Recommended Actions:")
                    for i, action in enumerate(response["actions"], 1):
                        st.write(f"{i}. {action}")
        else:
            st.warning("Please enter a question or description of your network issue.")

if __name__ == "__main__":
    main()
