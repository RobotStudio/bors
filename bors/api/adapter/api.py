"""
API Core
"""

from multiprocessing import Process

from bors.api.product import ApiProduct  # pylint: disable=E0611,E0401


def call_args(call, args=None):
    """If args are none, don't pass them"""
    return [call] if args is None else [call, args]


class ApiAdapter(ApiProduct):
    """Adapter for any API implementations"""
    is_connected_ws = False
    api = None

    def run(self):
        """Executed on startup of application"""
        self.api = self.context.get("cls")(self.context)
        self.context["inst"].append(self)  # Adapters used by strategies

        for call, calldata in self.context.get("calls", {}).items():
            def loop():
                """Loop on event scheduler, calling calls"""
                while not self.stopped.wait(calldata.get("delay", None)):
                    self.call(call, calldata.get("arguments", None))

            self.thread[call] = Process(target=loop)
            self.thread[call].start()

    def call(self, callname, arguments=None):
        """Executed on each scheduled iteration"""
        # Dynamically assigned for flexibility in implementations
        self.generate_result = getattr(self.api, "generate_result",
            self._generate_result)
        self.generate_request = getattr(self.api, "generate_request",
            self._generate_request)

        # See if a method override exists
        action = getattr(self.api, callname, None)
        if action is None:
            try:
                action = self.api.ENDPOINT_OVERRIDES.get(callname, None)
            except AttributeError:
                action = callname

        if not callable(action):
            request = self.generate_request(action, arguments)
            if action is None:
                self.api.call(*call_args(callname, arguments))
            else:
                self.api.call(*call_args(action, arguments))
        else:
            request = self.generate_request(callname, arguments)
            #self.generate_result(callname, action(request))
            action(request)

    def _generate_request(self, callname, request):
        """Generate a request object for delivery to the API"""
        # Retrieve path from API class
        schema = self.api.request_schema()
        schema.context['callname'] = callname
        return schema.dump(request).data.get("payload")

    def _generate_result(self, callname, result):
        """Generate a results object for delivery to the context object"""
        # Retrieve path from API class
        schema = self.api.result_schema()
        schema.context['callname'] = callname
        self.callback(schema.load(result), self.context)
