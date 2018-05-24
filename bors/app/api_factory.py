"""
API Core
"""

from bors.common.factory import BasicFactory

from bors.api.adapter.api import ApiAdapter
from bors.api.adapter.socketcluster import SCAdapter


class ApiMetaAdapter:
    """Adapter of adapters for all API instantiations"""
    name = "api"

    def __init__(self, contexts):
        self.apis = []  # type: list
        self.wsocks = []  # type: list

        for name, context in contexts.items():
            wsock = BasicFactory(SCAdapter)
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
