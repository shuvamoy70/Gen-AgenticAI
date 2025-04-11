"""
Configuration Module

This module handles loading and accessing configuration settings from YAML files
and environment variables.
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Global configuration dictionary
_config = {}

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file and environment variables.

    Args:
        config_path: Path to the configuration file. If None, uses default path.

    Returns:
        Dictionary containing configuration settings
    """
    global _config

    # Default config path
    if config_path is None:
        # Get the project root directory (parent of app directory)
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "settings.yaml"

    # Load configuration from YAML file
    try:
        with open(config_path, 'r') as file:
            _config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")
    except Exception as e:
        logger.error(f"Error loading configuration from {config_path}: {str(e)}")
        _config = {}

    # Override with environment variables if they exist
    # For example, if there's an env var MODEL_DEFAULT, it would override models.default
    for key, value in os.environ.items():
        if key.startswith("MODEL_"):
            section = "models"
            setting = key[6:].lower()  # Remove MODEL_ prefix and convert to lowercase
            if section not in _config:
                _config[section] = {}
            _config[section][setting] = value
            logger.debug(f"Overriding {section}.{setting} with environment variable {key}")
        elif key.startswith("APP_"):
            section = "app"
            setting = key[4:].lower()
            if section not in _config:
                _config[section] = {}
            _config[section][setting] = value
        elif key.startswith("AGENT_"):
            section = "agent"
            setting = key[6:].lower()
            if section not in _config:
                _config[section] = {}
            _config[section][setting] = value
        elif key.startswith("STREAMLIT_"):
            section = "streamlit"
            setting = key[10:].lower()
            if section not in _config:
                _config[section] = {}
            _config[section][setting] = value

    return _config

def get_config() -> Dict[str, Any]:
    """
    Get the current configuration.

    Returns:
        Dictionary containing configuration settings
    """
    global _config
    if not _config:
        load_config()
    return _config

def get_setting(section: str, default: Any = None) -> Any:
    """
    Get a specific section from the configuration.

    Args:
        section: The section of the configuration (e.g., 'models', 'app')
        default: Default value to return if the section is not found

    Returns:
        The section dictionary or the default value
    """
    config = get_config()
    try:
        return config.get(section, default)
    except Exception as e:
        logger.error(f"Error getting section {section}: {str(e)}")
        return default
