"""Configuration module"""

import os
import json
import importlib

from bors.config import default_settings


class Settings:
    """Application settings"""
    def __init__(self, settings_module):
        self.module = importlib.import_module(settings_module)

        self.configure(default_settings)
        self.configure(self.module)

    def configure(self, settings):
        for setting in dir(settings):
            if setting.isupper():
                setattr(self, setting, getattr(settings, setting))

    def get_api_services_by_name(self):
        """Return a dict of services by name"""
        if not self.services_by_name:
            self.services_by_name = dict({s.get('name'): s for s in self.conf
                                          .get("api")
                                          .get("services")})
        return self.services_by_name

    def get_api_credentials(self, apiname):
        """Returns a Credentials object for API access"""
        return self.get_api_service(apiname).get("credentials", None)

    def get_api_endpoints(self, apiname):
        """Returns the API endpoints"""
        try:
            return self.services_by_name\
                    .get(apiname)\
                    .get("endpoints")\
                    .copy()
        except AttributeError:
            raise Exception(f"Couldn't find the API endpoints")

    def get_ws_subscriptions(self, apiname):
        """Returns the websocket subscriptions"""
        try:
            return self.services_by_name\
                    .get(apiname)\
                    .get("subscriptions")\
                    .copy()
        except AttributeError:
            raise Exception(f"Couldn't find the websocket subscriptions")

    def get_api_calls(self):
        """Returns a list of calls to the api to generate the context object"""
        try:
            return self.conf.get("api").get("calls").copy()
        except:  # NOQA
            raise Exception(f"Couldn't find call list for APIs")

    def get_api(self, name=None):
        """Returns the API configuration"""
        if name is None:
            try:
                return self.conf.get("api").copy()
            except:  # NOQA
                raise Exception(f"Couldn't find the API configuration")

    def get_api_service(self, name=None):
        """Returns the specific service config definition"""
        try:
            svc = self.services_by_name.get(name, None)
            if svc is None:
                raise ValueError(f"Couldn't find the API service configuration")
            return svc
        except:  # NOQA
            raise Exception(f"Failed to retrieve the API service configuration")

    def get_log_level(self):
        """Returns the configured log level"""
        return self.conf.get("log_level", "INFO")


class AppConfig:
    """Application-wide configuration singleton"""
    services_by_name = {}  # type: dict

    def __init__(self, config=None):
        settings_module = os.environ.get('BORS_SETTINGS_MODULE')
        if not settings_module:
            raise ValueError('Unconfigured instance. Please use '
                             '`BORS_SETTINGS_MODULE` to specify the '
                             'configuration for your project.')

        self.settings = Settings(default_settings)
