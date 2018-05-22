"""
Build the context and pipeline; manage the API
"""
from bors.app.log import LoggerMixin
from bors.app.api_factory import ApiMetaAdapter
from bors.generics.context import ApiContextSchema, StrategyContextSchema


class AppBuilder(LoggerMixin):
    """Class that assembles and runs the application"""
    name = "builder"
    api_context_schema = ApiContextSchema
    strategy_context_schema = StrategyContextSchema

    def __init__(self, api_classes, strategy, app_config):
        self.conf = app_config

        self.api_contexts = {}  # type: dict

        self.exit = False

        self.create_logger()

        for api in self.conf.get_api_services_by_name().keys():
            self.log.debug(f"Found configured service: {api}")
            # Only build out APIs that have interfaces AND configurations
            for api_cls in api_classes:
                if api_cls.name == api:
                    self.api_contexts[api] = \
                        self.create_api_context(api_cls).data
                    break
                else:
                    self.log.debug(f"Skipping... {api}")

        self.api = ApiMetaAdapter(self.api_contexts)
        self.strat = strategy

    def create_api_context(self, cls):
        """Create and return an API context"""
        return self.api_context_schema().load({
            "name": cls.name,
            "cls": cls,
            "inst": [],
            "conf": self.conf.get_api_service(cls.name),
            "calls": self.conf.get_api_calls(),
            "shared": {},  # Used per-API to monitor state
            "log_level": self.conf.get_log_level(),
            "callback": self.receive
            })

    def run(self):
        """Run the queries and middleware pipeline"""
        # call run with receive callback function
        self.api.run()

    def receive(self, data, api_context):
        """Pass an API result down the pipeline"""
        self.log.debug(f"Putting data on the pipeline: {data}")
        result = {
            "api_contexts": self.api_contexts,
            "api_context": api_context,
            "strategy": dict(),  # Shared strategy data
            "result": data,
            "log_level": api_context["log_level"],
        }
        self.strat.execute(self.strategy_context_schema().load(result).data)

    def shutdown(self, signum, frame):  # pylint: disable=unused-argument
        """Shut it down"""
        if not self.exit:
            self.exit = True
            self.log.debug(f"SIGTRAP!{signum};{frame}")
            self.api.shutdown()
            self.strat.shutdown()
