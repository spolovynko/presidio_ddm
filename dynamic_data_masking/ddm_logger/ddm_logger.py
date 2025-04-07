import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from threading import Lock

class DynamicDataMaskingLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, name="dynamic_data_masking", level=logging.INFO):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DynamicDataMaskingLogger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, name="dynamic_data_masking", level=logging.INFO):
        if self._initialized:
            return

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{name}_{date_str}.log"
        log_path = os.path.join(log_dir, log_filename)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Daily File Handler
        file_handler = TimedRotatingFileHandler(
            filename=log_path,
            when="midnight", # Rotate at midnight
            interval=1, # Every 1 day
            backupCount=30, # Keep last 7 logs
            encoding="utf-8",
            utc=False # Set to True if you're working in UTC
        )
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y-%m-%d" # Log file format: dynamic_data_masking.log.2025-04-02
        self.logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self._initialized = True

    def get_logger(self):
        return self.logger