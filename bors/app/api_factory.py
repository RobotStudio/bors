"""
API Core
"""

from bors.app.log import LoggerMixin
from bors.common.factory import BasicFactory

from bors.api.adapter.api import ApiAdapter
from bors.api.adapter.ws import WsAdapter


class ApiMetaAdapter(LoggerMixin):
    """Adapter of adapters for all API instantiations"""
    name = "api"

    def __init__(self, contexts):
        self.apis = []  # type: list
        self.wsocks = []  # type: list

        self.create_logger()

        for name, context in contexts.items():
            self.log.debug(f"Starting API: {name}")
            self.log.debug(f"{name}: {context}")

            wsock = BasicFactory(WsAdapter)
            wsock.product.interface(context)
            self.wsocks.append(wsock.product)

            api = BasicFactory(ApiAdapter)
            api.product.interface(context)
            self.apis.append(api.product)

    def run(self):
        """Executed on startup of application"""
        for wsock in self.wsocks:
            wsock.run()
        for api in self.apis:
            api.run()

    def shutdown(self):
        """Executed on shutdown of application"""
        for wsock in self.wsocks:
            wsock.shutdown()
        for api in self.apis:
            api.shutdown()
