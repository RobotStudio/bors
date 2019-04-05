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
    """Test the CLI version."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['version'])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_generate_help():
    """Test the CLI generator help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['generate', '--help'])
    assert result.exit_code == 0
    assert ' generate [OPTIONS] COMMAND [ARGS]' in result.output
    assert 'Generate a new project for use with ' in result.output


def test_cli_generate_api_help():
    """Test the CLI generator help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['generate', 'api', '--help'])
    assert result.exit_code == 0
    assert ' generate api [OPTIONS] APINAME' in result.output
    assert 'Commands:' not in result.output


def test_cli_generate_api_help_on_fail():
    """Test the CLI generator help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['generate', 'api'])
    assert result.exit_code == 2
    assert ' generate api [OPTIONS] APINAME' in result.output
    assert 'Error: Missing argument "apiname".' in result.output
