#!/usr/bin/env python3

"""Used to validate that thing work as expected"""

from bors.app.strategy import IStrategy
from bors.app.config import AppConfig
from bors.app.builder import AppBuilder
from bors.app.strategy import Strategy

from bors.algorithms.echo import echo
from bors.common.dotobj import DotObj


class Print(IStrategy):
    """Print strategy implementation"""
    def bind(self, context):
        """
        Bind the strategy to the middleware pipeline returning the context
        """
        echo(f"""PrintStrategy: {context['result'].data['callname']}""")

        # just a pass-through
        return context


class Request:
    """A bare request object"""
    def __init__(self, **kwargs):
        self.callname = kwargs.get('callname', None)
        self.payload = kwargs.get('payload', None)


class Result(DotObj):
    """A bare result object"""
    def __init__(self, **kwargs):
        self.callname = kwargs.get('callname', None)
        self.channel = kwargs.get('channel', None)
        self.response_type = kwargs.get('response_type', None)
        self.result = kwargs.get('result', None)
        self.errors = kwargs.get('errors', None)
        super().__init__(**kwargs)


class MyAPI:
    """
    Mock API (doesn't do anything, but drop a message on the pipeline upon
    request.
    """
    name = "my_api"

    def __init__(self, context):
        self.request = Request
        self.result = Result
        self.context = context

    def call(self, callname, data=None, **args):
        """Mock call interface"""
        return {"test": "Success", "call": callname}


def main():
    """MAIN"""
    config = {
        "api": {
            "services": [
                {
                    "name": "my_api",
                    "testkey": "testval",
                },
            ],
            "calls": {
                "hello_world": {
                    "delay": 5,
                    "priority": 1,
                    "arguments": None,
                },
                "marco": {
                    "delay": 1,
                    "priority": 1,
                },
                "pollo": {
                    "delay": 1,
                    "priority": 1,
                },
            }
        }
    }
    app = AppBuilder([MyAPI], Strategy(Print()), AppConfig(config))
    app.run()


if __name__ == "__main__":
    main()
