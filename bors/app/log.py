"""Log Util"""

import logging

from bors.app.config import AppConf


class LoggerMixin:
    """Mixin to be used to simplify the logging interface"""
    def create_logger(self):
        """Generates a logger instance from the singleton"""
        name = "bors"
        if hasattr(self, "name"):
            name = self.name

        conf = AppConf()
        self.log = logging.getLogger(name)
        self.log.setLevel(
            getattr(logging, conf.get_log_level(), logging.INFO))
