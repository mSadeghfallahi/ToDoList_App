"""Logging configuration and utilities for the To-Do List Application."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class LogConfig:
    """Configuration class for application logging."""
    
    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    # Default log format
    DEFAULT_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Detailed log format for debugging
    DETAILED_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "[%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s"
    )


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    detailed_format: bool = False
) -> logging.Logger:
    """Setup a logger with console and optional file handlers.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        log_file: Path to log file (optional). If provided, logs to file as well.
        detailed_format: If True, use detailed format with file/line numbers
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Format
    log_format = LogConfig.DETAILED_FORMAT if detailed_format else LogConfig.DEFAULT_FORMAT
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
