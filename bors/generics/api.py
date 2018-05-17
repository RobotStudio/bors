"""Generic API schemas"""

from marshmallow import Schema, post_load
from marshmallow import fields as f

from bors.common.dotobj import DotObj


class GenericObject(DotObj):
    """Generic object with dot or hash style get/set"""
    pass


class GenericSchema(Schema):
    """Schema from which all other schemas should inherit"""
    @post_load
    def make_object(self, data):  # pylint: disable=no-self-use
        """Generate an object for passing to the API"""
        return GenericObject(data)


class ApiFacadeSchema(GenericSchema):
    """Used to define an API integration (facade)"""
    name = f.Str(required=True)
    call = f.Method(required=True)


class RequestSchema(GenericSchema):
    """Generic API result (inherit to use a schema for result creation)"""
    class Meta:
        """All results should be strict"""
        strict = True


class ResultSchema(GenericSchema):
    """Generic API result (inherit to use a schema for result creation)"""
    class Meta:
        """All results should be strict"""
        strict = True
