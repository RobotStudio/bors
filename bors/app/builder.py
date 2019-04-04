"""
Build the context and pipeline; manage the API
"""
from bors.app.api_factory import ApiMetaAdapter
from bors.app.config import settings
from bors.app import logger


class AppBuilder:
    """Class that assembles and runs the application"""
    loaded_modules: list = {}

    apis: tuple = ()
    middlewares: tuple = ()
    transports: tuple = ()
    apps: tuple = ()

    def __init__(self):
        for import_type in settings.import_types:
            for entry in getattr(settings, import_type):
                self.load(import_type, entry)

    def load(self, import_type, module):


        #for api in settings.get_api_services_by_name().keys():
        #    logger.debug(f"Found configured service: {api}")
        #    # Only build out APIs that have interfaces AND configurations
        #    for api_cls in api_classes:
        #        if api_cls.name == api:
        #            self.api_contexts[api] = \
        #                self.create_api_context(api_cls).data
        #            break
        #        else:
        #            logger.debug(f"Skipping... {api}")

        self.api = ApiMetaAdapter(self.loaded_modules['API_ADAPTERS'])
        #self.strat = strategy

    def create_api_context(self, cls):
        """Create and return an API context"""
        return {
            "name": cls.name,
            "cls": cls,
            "inst": [],
            "conf": settings.get_api_service(cls.name),
            "calls": self.settings.get_api_calls(),
            "shared": {},  # Used per-API to monitor state
            "log_level": self.settings.get_log_level(),
            "callback": self.receive
        }

    def run(self):
        """Run the queries and middleware pipeline"""
        # call run with receive callback function
        self.api.run()

    def receive(self, data, api_context):
        """Pass an API result down the pipeline"""
        logger.debug(f"Putting data on the pipeline: {data}")
        self.strat.execute({
            "api_contexts": self.api_contexts,
            "api_context": api_context,
            "strategy": dict(),  # Shared strategy data
            "result": data,
            "log_level": api_context["log_level"],
        })

    def shutdown(self, signum, frame):  # pylint: disable=unused-argument
        """Shut it down"""
        if not self.exit:
            self.exit = True
            logger.debug(f"SIGTRAP!{signum};{frame}")
            self.api.shutdown()
            self.strat.shutdown()
