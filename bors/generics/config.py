"""Configuration definition"""

from marshmallow import Schema, fields, post_load

from bors.common.dotobj import DotObj


class Conf(DotObj):
    """Loads a sane configuration"""
    def __init__(self, **config):
        self.conf = config

    def get(self, *args, **kwargs):
        """Get something"""
        return self.conf.get(*args, **kwargs)


class ApiServiceConfSchema(Schema):
    """API service configuration object"""
    name = fields.Str(required=True)


class ApiConfSchema(Schema):
    """API configuration object"""
    calls = fields.Dict()
    services = fields.List(fields.Nested(ApiServiceConfSchema()))


class ConfSchema(Schema):
    """Root configuration schema"""
    log_level = fields.Str()
    api = fields.Nested(ApiConfSchema())

    @post_load
    def make_conf(self, data):  # pylint: disable=R0201
        """Generate a configuration object"""
        return Conf(**data)

    class Meta:
        """Make sure that we bail if we can't parse"""
        strict = True
