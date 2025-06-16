# core/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

FORMATTER = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")

    if not logger.hasHandlers():
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
        console_handler = logging.StreamHandler()

        file_handler.setFormatter(FORMATTER)
        console_handler.setFormatter(FORMATTER)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
