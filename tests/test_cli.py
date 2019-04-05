#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bors` package."""

import pytest

from click.testing import CliRunner

from bors import bors, __version__
from bors import cli


def test_cli_usage():
    """Test the CLI usage."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: ' in result.output

def test_cli_help():
    """Test the CLI help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--help'])
    assert result.exit_code == 0
    assert '--help ' in result.output
    assert 'Show this message and exit.' in result.output

def test_cli_version():
    """Test the CLI help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output
