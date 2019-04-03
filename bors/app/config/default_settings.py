"""Default application settings"""


DEBUG: bool = False
"""Will set the log level to DEBUG if set to True"""


RATE_LIMIT: float = 1
"""Global rate limit to use.  This gets overriden by the API plugins."""


API_PLUGINS: list = []
"""API interfacing modules to include in the application."""


MIDDLEWARES: list = []
"""Middleware modules to execute strategies in incumbant data."""
