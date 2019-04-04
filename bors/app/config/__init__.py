"""Config initialization"""

from bors.app.config.base import Settings, AppConfig


settings = Settings()  # NOQA

__all__ = ('settings', 'AppConfig')
