# -*- coding: utf-8 -*-

"""Console script for bors."""
import os
import sys
import click

from bors.bors import Bors


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_PATH = os.path.join(ROOT_DIR, 'templates')


@click.group()
@click.option('-V', '--version', is_flag=True, help='Display version and exit')
def main(version):
    """Console script for bors.
    """
    if version:
        click.echo(__version__)
    return 0


@main.group()
def run():
    """Execute the bors framework"""
    try:
        bors = Bors()
        bors.execute()
    except KeyboardInterrupt:
        click.echo("Shutting down...")
        bors.shutdown()


@main.group()
def generate():
    """Generate a new project for use with ``bors``."""
    pass


@generate.command()
@click.argument('APIName', help='The name of the API to integrate with.')
def api():
    """Generate stubs for interacting with an API"""
    click.echo("Generating an API")

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
