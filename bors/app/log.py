"""Log Util"""

import os
import logging


def getlogger():
    """Create a global logger instance"""
    logger = logging.getLogger(__name__)
    level = getattr(logging, os.environ.get('BORS_LOGLEVEL', 'INFO'))
    logger.setLevel(level)
    return logger


logger = getlogger()  # NOQA
