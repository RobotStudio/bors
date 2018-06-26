from bors.common.dotobj import DotObj

class DerivedDotObj(DotObj):
    attrib = "value"


def test_dotobj_like_dict():
    a = DerivedDotObj({"AAA": 123})
    assert a.AAA == a["AAA"]

def test_dict_like_dotobj():
    a = DerivedDotObj()
    a.AAA = 123
    assert a.AAA == a["AAA"]
