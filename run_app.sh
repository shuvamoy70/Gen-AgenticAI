#!/bin/bash

# Run the Network AI Assistant Streamlit app

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if requirements are installed
if ! pip list | grep -q streamlit; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
echo "Starting Network AI Assistant..."
streamlit run main.py
