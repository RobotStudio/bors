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
        # See if a method override exists
        action = getattr(self.api, callname, None)
        if action is None:
            try:
                action = self.api.ENDPOINT_OVERRIDES.get(callname, None)
            except AttributeError:
                action = callname

        if not callable(action):
            request = self._generate_request(action, arguments)
            if action is None:
                return self._generate_result(
                    callname, self.api.call(*call_args(callname, arguments)))
            return self._generate_result(
                callname, self.api.call(*call_args(action, arguments)))

        request = self._generate_request(callname, arguments)
        return self._generate_result(callname, action(request))

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
