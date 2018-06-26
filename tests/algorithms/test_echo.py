from bors.algorithms.echo import echo

def test_echo_algorithm():
    assert echo("This is a test") is None
