import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration from environment variables"""
    MAX_NUMBER_OF_PROJECTS = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 10))