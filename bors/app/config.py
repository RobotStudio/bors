"""Configuration module"""

import json
from collections import namedtuple

from bors.common.dict_merge import dict_merge
from bors.generics.config import ConfSchema


DEFAULT_CONFIG = {
    "api": {
        "ratelimit": 1,
        "services": [],  # API services to interact with
        "calls": {},  # Calls made to the given API
    },
    "log_level": "INFO",
}


class AppConf:
    """Application-wide configuration singleton"""
    conf = None
    raw_conf = None
    services_by_name = {}  # type: dict

    def __init__(self, config=None):
        global DEFAULT_CONFIG
        self.raw_conf = DEFAULT_CONFIG.copy()

        try:
            conf = json.loads(config)
        except ValueError:
            conf = config

        dict_merge(self.raw_conf, conf)
        self.conf = ConfSchema().load(self.raw_conf).data

    def get_api_services_by_name(self):
        """Return a dict of services by name"""
        if not self.services_by_name:
            self.services_by_name = {s.get('name'): s for s in self.conf
                                     .get("api")
                                     .get("services")}
        return self.services_by_name

    def get_api_credentials(self, apiname):
        """Returns a Credentials object for API access"""
        try:
            return self.data\
                .get("api")\
                .get("services")\
                .get(apiname)\
                .get("credentials")\
                .copy()

        except AttributeError:
            raise Exception(f"Couldn't find credentials for API: {apiname}")

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
        try:
            return self.services_by_name.get(name).copy()
        except:  # NOQA
            raise Exception(f"Couldn't find the API configuration")

    def get_log_level(self):
        """Returns the configured log level"""
        return self.conf.get("log_level", "INFO")
