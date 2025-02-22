import logging
from config.settings import LOG_LEVEL

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create logger
    logger = logging.getLogger(__name__)
    return logger

# Create a logger instance that can be imported by other modules
logger = setup_logging() 