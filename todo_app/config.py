import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
# Find the project root (where .env file is located)
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration from environment variables"""
    MAX_NUMBER_OF_PROJECTS = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 10))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    # Allow overriding the full DATABASE_URL (useful for tests / alternate DBs)
    DATABASE_URL = os.getenv("DATABASE_URL") or (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # CLI deprecation configuration
    # Optional env var to set a hard deprecation date (YYYY-MM-DD) shown to users
    CLI_DEPRECATION_DATE = os.getenv('CLI_DEPRECATION_DATE', '2026-01-01')
    # By default, show CLI deprecation warning; set to 'true' to disable warnings
    DISABLE_CLI_DEPRECATION_WARNING = os.getenv('DISABLE_CLI_DEPRECATION_WARNING', 'false').lower() == 'true'