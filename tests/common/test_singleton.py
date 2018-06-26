from bors.common.singleton import Singleton


class TestSingleton(metaclass=Singleton):
    attrib = "test_this"

def test_multiple_instantiations():
    a = TestSingleton()
    b = TestSingleton()
    assert a == b

def test_multiple_instantiation_assignments():
    a = TestSingleton()
    b = TestSingleton()
    a.attrib = "new_test"
    assert a == b
    assert a.attrib == b.attrib
