"""
Network AI Assistant - Main Entry Point

This is the main entry point for the Network AI Assistant application.
It initializes the Streamlit app and sets up the agent environment.
"""
import streamlit as st
from app.agents.network_agent import NetworkAgent
from app.utils.logger import setup_logger
from app.utils.config import load_config

# Setup logging
logger = setup_logger()

# Load configuration
config = load_config()

def main():
    """
    Main function to run the Network AI Assistant application.
    """
    # Get Streamlit settings from config
    streamlit_config = config.get('streamlit', {})

    st.set_page_config(
        page_title=streamlit_config.get('page_title', "Network AI Assistant"),
        page_icon=streamlit_config.get('page_icon', "🌐"),
        layout=streamlit_config.get('layout', "wide"),
        initial_sidebar_state=streamlit_config.get('initial_sidebar_state', "expanded")
    )

    # Apply theme if configured
    if 'theme' in streamlit_config:
        theme = streamlit_config['theme']
        # Note: Streamlit theme can only be set via config.toml, but we can show the configured values
        logger.info(f"Theme settings from config: {theme}")

    # Title and description are set below using config values

    # Get app and model settings from config
    app_config = config.get('app', {})
    models_config = config.get('models', {})

    # Get app name and description from config
    app_name = app_config.get('name', "Network AI Assistant")
    app_description = app_config.get('description', "An Agentic AI Solution for Network Management")

    # Update title and description from config
    st.title(f"🌐 {app_name}")
    st.subheader(app_description)

    # Sidebar for configuration
    st.sidebar.title("Configuration")

    # Get available models from config
    default_model = models_config.get('default', "HuggingFace/distilbert-base-uncased")
    alternative_models = models_config.get('alternatives', [])
    available_models = [default_model] + alternative_models

    # Model selection dropdown
    model_option = st.sidebar.selectbox(
        "Select AI Model",
        available_models
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
