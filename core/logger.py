import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, logs_dir: str):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("solomon")
        self.logger.setLevel(logging.INFO)
        
        # Avoid adding multiple handlers if Logger is instantiated multiple times
        if not self.logger.handlers:
            self._setup_handler()

    def _get_log_file(self) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.logs_dir / f"{today}.log"

    def _setup_handler(self):
        log_file = self._get_log_file()
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message: str, *args):
        if args:
            try:
                formatted_message = message % args
            except TypeError:
                formatted_message = f"{message} {args}"
        else:
            formatted_message = message
        
        self.logger.info(formatted_message)

    def log_task_output(self, task_id: str, output: bytes):
        try:
            decoded_output = output.decode("utf-8").strip()
            if decoded_output:
                self.log(f"TASK OUTPUT [%s]:\n%s", task_id, decoded_output)
        except Exception as e:
            self.log("ERROR: Failed to log task output for %s: %s", task_id, str(e))
