"""Configuration definition"""

from marshmallow import Schema, fields, post_load


class Conf:
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
    """Log configuration object"""
    calls = fields.Dict()
    services = fields.List(fields.Nested(ApiServiceConfSchema()))


class LogConfSchema(Schema):
    """Log configuration object"""
    level = fields.Str()
    modules = fields.Dict(
        fields.Nested('self',
                      many=True,
                      exclude=('modules',),
                      default=None)
        )


class ConfSchema(Schema):
    """Root configuration schema"""
    logger = fields.Nested(LogConfSchema())
    api = fields.Nested(ApiConfSchema())

    @post_load
    def make_conf(self, data):  # pylint: disable=R0201
        """Generate a configuration object"""
        return Conf(**data)

    class Meta:
        """Make sure that we bail if we can't parse"""
        strict = True
