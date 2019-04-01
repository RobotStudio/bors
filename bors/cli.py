# -*- coding: utf-8 -*-

"""Console script for bors."""
import os
import sys
import click


@click.group()
@click.option('-V', '--version', is_flag=True, help='Display version and exit')
def main(version):
    """Console script for bors.
    """
    if version:
        click.echo(__version__)
    return 0


@main.group()
def generate():
    click.echo(os.path.dirname(os.path.abspath(__file__)))


@generate.command()
def api():
    click.echo("Generating an API")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
