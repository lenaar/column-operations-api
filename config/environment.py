"""
Environment configuration for Column Operations API
"""
import os

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
TABLE_NAME = os.getenv("TABLE_NAME", "data_table")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = os.getenv("API_TITLE", "Column Operations API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

# Development Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
