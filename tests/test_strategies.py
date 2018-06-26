from bors.strategies.echo import Echo
from bors.strategies.print import Print

def test_echo_strategy():
    strategy = Echo()
    data = {"test": 123}
    assert strategy.bind(data) == data

def test_print_strategy():
    strategy = Print()
    data = {"test": 123}
    assert strategy.bind(data) == data
