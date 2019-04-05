"""Config initialization"""

from bors.config.app import AppConfig
from bors.config.settings import Settings


settings = Settings()  # NOQA

__all__ = ('settings', 'Settings', 'AppConfig')
