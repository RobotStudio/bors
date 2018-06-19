"""
Simple echo strategy to output an "ECHO"
"""

from bors.app.strategy import IStrategy
from bors.algorithms.echo import echo


class Echo(IStrategy):
    """Echo Strategy implementation"""
    def bind(self, context):
        """
        Bind the strategy to the middleware pipeline,
        returning the context
        """
        echo("ECHO!")

        # just a pass-through
        return context
