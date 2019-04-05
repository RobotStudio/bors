"""Configuration module"""

import os


class AppConfig:
    """Application configuration base"""
    services_by_name = {}  # type: dict

    def __init__(self, config=None):
        settings_module = os.environ.get('BORS_SETTINGS_MODULE')
        if not settings_module:
            raise ValueError('Unconfigured instance. Please use '
                             '`BORS_SETTINGS_MODULE` to specify the '
                             'configuration for your project.')

        self.settings = Settings(default_settings)
