"""
API Core
"""

from multiprocessing import Event


class ApiProduct:
    """ApiAdapterFactory Product interface"""
    api = None
    context = None
    callback = None

    thread = {}  # type: dict
    keep_going = True
    stopped = Event()

    def interface(self, context):
        """Implement the interface for the adapter object"""
        self.context = context
        self.callback = self.context.get("callback")

    def shutdown(self):
        """Executed on shutdown of application"""
        self.stopped.set()

        if hasattr(self.api, "shutdown"):
            self.api.shutdown()

        for thread in self.thread.values():
            thread.join()
