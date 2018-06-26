from bors.common.dict_merge import dict_merge


def test_overwrite_key():
    data1 = {"AAA": 111}
    data2 = {"AAA": 222, "BBB": 333}
    dict_merge(data1, data2)
    assert data1 == data2


def test_merge():
    data1 = {"AAA": 111}
    data2 = {"BBB": 222, "CCC": 333}

    dict_merge(data1, data2)
    for key, val in data2.items():
        assert data1[key] == val

    assert "AAA" not in data2
