from bors.common.factory import Creator, Product, BasicFactory

class Adapter():
    attrib = "test"
    context = None

    def interface(self, context):
        self.context = context

def test_factory_interface():
    context = {"AAA": 111, "BBB": 222}
    factory = BasicFactory(Adapter)
    factory.product.interface(context)
    assert factory.product.attrib == "test"
    assert context == factory.product.context
