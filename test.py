#!/usr/bin/env python3

"""Used to validate that thing work as expected"""

from marshmallow import Schema, fields, post_load

from bors.app.strategy import IStrategy
from bors.app.config import AppConf
from bors.app.builder import AppBuilder
from bors.app.strategy import Strategy

from bors.algorithms.echo import echo
from bors.common.dotobj import DotObj


class MockItemSchema(Schema):
    """Mock item"""
    test = fields.Str(required=True)
    call = fields.Str(required=True)


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


class RequestSchema(Schema):
    """Schema defining the data structure the API can be called with"""
    callname = fields.Str(required=True)
    payload = fields.Dict()

    @post_load
    def make_request(self, data):
        """Parse the outgoing schema"""
        sch = MockItemSchema()
        return Request(**{
            "callname": self.context.get("callname"),
            "payload": sch.dump(data),
        })

    class Meta:
        """Strict"""
        strict = True


class ResponseSchema(Schema):
    """Schema defining the data structure the API can be called with"""
    @post_load
    def populate_data(self, data):
        """Parse the outgoing schema"""
        sch = MockItemSchema()
        return Result(**{
            "callname": self.context.get("callname"),
            "result": sch.dump(data),
        })

    class Meta:
        """Strict"""
        strict = True


class MyAPI:
    """
    Mock API (doesn't do anything, but drop a message on the pipeline upon
    request.
    """
    name = "my_api"

    def __init__(self, context):
        self.request_schema = RequestSchema
        self.result_schema = ResponseSchema
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
    app = AppBuilder([MyAPI], Strategy(Print()), AppConf(config))
    app.run()


if __name__ == "__main__":
    main()
