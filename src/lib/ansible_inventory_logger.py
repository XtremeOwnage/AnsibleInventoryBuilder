import logging
import inspect
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from globals import (LOG_FORMAT, CUSTOM_LOG_FORMAT, EXIT_ON_ERROR, EXIT_ON_FATAL, ENABLE_FILE_LOGGING, LOG_FILE_PATH, LOG_FILE_MAX_SIZE, LOG_TIMESTAMP_FORMAT, LOG_FILE_BACKUP_COUNT, ENABLE_LOG_ROTATION, MIN_LOG_LEVEL)

class InventoryLogger:
    def __init__(self, level=MIN_LOG_LEVEL):
        """Initialize the logger with configurable settings and handlers."""
        # Create and configure the logger
        self.logger = logging.getLogger('InventoryLogger')
        self.logger.setLevel(level)
        self.logger.propagate = False  # Prevent log messages from being propagated to the root logger

        # Check if the logger already has handlers and remove them to avoid duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Set up console handler with the format from global settings
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_TIMESTAMP_FORMAT)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Set up file handler if enabled
        if ENABLE_FILE_LOGGING:
            if ENABLE_LOG_ROTATION:
                file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=LOG_FILE_MAX_SIZE, backupCount=LOG_FILE_BACKUP_COUNT)
            else:
                file_handler = logging.FileHandler(LOG_FILE_PATH)
            file_handler.setLevel(level)
            file_handler.setFormatter(console_formatter)
            self.logger.addHandler(file_handler)

    def log(self, level, message):
        """Log a message with the specified level and custom formatting."""
        # Extract module and method from the call stack
        frame = inspect.stack()[2]
        module = Path(frame.filename).name
        method = frame.function
        formatted_message = CUSTOM_LOG_FORMAT.format(module=module, method=method, message=message)
        self.logger.log(level, formatted_message)
        
        # Handle exit conditions based on log level
        if (level == logging.ERROR and EXIT_ON_ERROR) or (level == logging.CRITICAL and EXIT_ON_FATAL):
            sys.exit(1)

    def verbose(self, message):
        self.log(logging.DEBUG, f"[VERBOSE]: {message}")

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def warning(self, message):
        self.log(logging.WARNING, message)

    def fatal(self, message):
        self.log(logging.FATAL, message)

    def critical(self, message):
        self.log(logging.CRITICAL, message)

# Create a logger instance to use throughout your application
logger = InventoryLogger()
