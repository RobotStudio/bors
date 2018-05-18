"""Log Util"""

import logging


class LoggerMixin:
    """Mixin to be used to simplify the logging interface"""
    def create_logger(self):
        """Generates a logger instance from the singleton"""
        name = "bors"
        if hasattr(self, "name"):
            name = self.name
        self.log = logging.getLogger(name)
