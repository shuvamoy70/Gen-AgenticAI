"""
Logger Module

This module provides logging functionality for the application.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure the root logger
def setup_logger():
    """
    Set up and configure the application logger.
    
    Returns:
        The configured logger instance
    """
    # Create a logger
    logger = logging.getLogger("network_ai_assistant")
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create a timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = RotatingFileHandler(
        f"logs/app_{timestamp}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Set formatters
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name=None):
    """
    Get a logger instance.
    
    Args:
        name: The name for the logger, typically the module name
        
    Returns:
        A logger instance
    """
    if name:
        return logging.getLogger(f"network_ai_assistant.{name}")
    return logging.getLogger("network_ai_assistant")
