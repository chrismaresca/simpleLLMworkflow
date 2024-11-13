import logging
import os
from datetime import datetime

# Ensure the logs directory exists
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

class LoggerSingleton:
    _instance = None
    _log_file_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("app_logger")
            cls._instance.logger.setLevel(logging.INFO)
        return cls._instance

    def _initialize_log_file(self):
        """Initialize the log file lazily when the first log is written."""
        if not self._log_file_initialized:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self._log_file_initialized = True

    def get_logger(self):
        """Public method to get the logger instance."""
        self._initialize_log_file()
        return self.logger

    @staticmethod
    def get_log_file_path():
        """Get the log file path for deletion check."""
        return log_file


# Initialize the logger globally
logger = LoggerSingleton().get_logger()
