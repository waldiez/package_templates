# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Tests for my_package.cli.*."""

import os
import sys
from typing import Callable, Generator
from unittest.mock import patch

import pytest
from flask import Flask
from typer.testing import CliRunner

from my_package.cli import app, get_default_port

runner = CliRunner()


@pytest.fixture(name="backup_and_restore_port_env")
def backup_and_restore_port_env_fixture() -> Generator[None, None, None]:
    """Backup and restore the port environment variable.

    Yields
    ------
    None
        The generator yields control back to the test function.
    """
    port = os.environ.get("MY_PACKAGE_PORT")
    yield
    if port is not None:
        os.environ["MY_PACKAGE_PORT"] = port
    else:
        os.environ.pop("MY_PACKAGE_PORT", None)


def test_cli_help(escape_ansi: Callable[[str], str]) -> None:
    """Test the CLI help message.

    Parameters
    ----------
    escape_ansi : Callable[[str], str]
        The escape_ansi fixture (defined in conftest.py).
    """
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    escaped_output = escape_ansi(result.output)
    assert "Usage" in escaped_output
    assert "--version" in escaped_output
    assert "run" in escaped_output


def test_cli_version(escape_ansi: Callable[[str], str]) -> None:
    """Test the CLI version flag.

    Parameters
    ----------
    escape_ansi : Callable[[str], str]
        The escape_ansi fixture (defined in conftest.py).
    """
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "my-package" in escape_ansi(result.output)


def test_cli_run() -> None:
    """Test the CLI run command."""
    with patch("my_package.main.serve") as mock_serve:
        mock_serve.side_effect = lambda *args, **kwargs: None
        result = runner.invoke(app, ["run"])
        mock_serve.assert_called_once()
        assert result.exit_code == 0


def test_cli_run_port() -> None:
    """Test the CLI run command with a custom port."""
    with patch("my_package.main.serve") as mock_serve:
        mock_serve.side_effect = lambda *args, **kwargs: None
        result = runner.invoke(app, ["run", "--port", "1234"])
        mock_serve.assert_called_once()
        assert result.exit_code == 0


def test_cli_run_dev(
    flask_app: Flask,
) -> None:
    """Test the CLI run command with the dev flag.

    Parameters
    ----------
    flask_app : MagicMock
        The mock Flask app fixture.
    """
    with patch("my_package.main.create_app", return_value=flask_app):
        result = runner.invoke(app, ["run", "--dev", "--port", "5000"])
        assert result.exit_code == 1


def test_get_default_port() -> None:
    """Test the get_default_port function."""
    assert get_default_port() == 8000
    with patch.dict("os.environ", {"MY_PACKAGE_PORT": "1234"}):
        assert get_default_port() == 1234
    with patch.dict("os.environ", {"MY_PACKAGE_PORT": "abc"}):
        assert get_default_port() == 8000


# pylint: disable=unused-argument
def test_get_default_port_cli(
    backup_and_restore_port_env: Generator[None, None, None],
) -> None:
    """Test the get_default_port function with CLI arguments.

    Parameters
    ----------
    backup_and_restore_port_env : Generator[None, None, None]
        The backup_and_restore_port_env fixture.
    """
    with patch.object(sys, "argv", ["--port", "2345"]):
        assert get_default_port() == 2345


# pylint: disable=unused-argument
def test_get_default_port_cli_invalid(
    backup_and_restore_port_env: Generator[None, None, None],
) -> None:
    """Test the get_default_port function with invalid CLI arguments.

    Parameters
    ----------
    backup_and_restore_port_env : Generator[None, None, None]
        The backup_and_restore_port_env fixture.
    """
    with patch.object(sys, "argv", ["--port", "abc"]):
        assert get_default_port() == 8000


# pylint: disable=unused-argument
def test_get_default_port_cli_missing(
    backup_and_restore_port_env: Generator[None, None, None],
) -> None:
    """Test the get_default_port function with missing CLI arguments.

    Parameters
    ----------
    backup_and_restore_port_env : Generator[None, None, None]
        The backup_and_restore_port_env fixture.
    """
    with patch.object(sys, "argv", ["--port"]):
        assert get_default_port() == 8000
