# -*- coding: utf-8 -*-

"""Console script for bors."""
import os
import sys
import click

from bors import __version__
from bors.bors import Bors


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_PATH = os.path.join(ROOT_DIR, 'templates')


def show_help():
    """Display the help using click.echo"""
    command = click.get_current_context().command
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


@click.group()
def main():
    """Console script for bors."""
    return 0


@main.command()
def version():
    """Display the version and exit."""
    click.echo(__version__)
    return 0


@main.group()
def run():
    """Launch the bors framework."""
    try:
        bors = Bors()
        bors.execute()
    except KeyboardInterrupt:
        click.echo("Shutting down...")
        bors.shutdown()
    finally:
        return 0


@main.group()
def generate():
    """Generate a new project for use with bors."""
    return 0


@generate.command()
@click.argument('apiname') #, help='The name of the API to integrate with.')
def api(apiname):
    """Generate stubs for interacting with an API."""
    click.echo("Generating an API.")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
