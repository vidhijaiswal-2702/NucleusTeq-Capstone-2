import logging
from logging.handlers import RotatingFileHandler
import os

# Directory where all log files will be stored
LOG_DIR = "logs"
# Create the directory if it doesn't already exist
os.makedirs(LOG_DIR, exist_ok=True)

# Log message format: includes timestamp, log level, module name, and message
FORMATTER = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a logger configured for a specific module.
    
    It writes logs to a file (rotating when large) and also outputs to the console.
    Useful for debugging and monitoring during development and production.

    Args:
        module_name (str): Name of the module or file using the logger (e.g., "auth", "orders").

    Returns:
        logging.Logger: A fully configured logger object.
    """
    # Get (or create) a logger with the specified name
    logger = logging.getLogger(module_name)
    # Set minimum log level to DEBUG (shows everything: DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)
    
    # Full path to the log file, e.g., logs/auth.log
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")

    # Prevent adding multiple handlers if logger is already set up
    if not logger.hasHandlers():
        # File handler with rotation: max 5MB per file, keep up to 3 backup files
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
        
        # Console handler to also show logs in the terminal
        console_handler = logging.StreamHandler()

        # Apply the formatter to both handlers
        file_handler.setFormatter(FORMATTER)
        console_handler.setFormatter(FORMATTER)

        # Attach handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Return the configured logger
    return logger

