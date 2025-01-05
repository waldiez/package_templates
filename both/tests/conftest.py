# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Configuration for pytest."""

import re
from typing import Callable, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from my_package.main import create_app


@pytest.fixture(name="flask_app")
def app_fixture() -> Generator[Flask, None, None]:
    """Create a Flask app for testing.

    Yields
    ------
    Generator[Flask, None, None]
        The Flask app.
    """
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app


@pytest.fixture()
def client(flask_app: Flask) -> FlaskClient:
    """Create a test client for the Flask app.

    Parameters
    ----------
    flask_app : Flask
        The Flask app.

    Returns
    -------
    FlaskClient
        The test client.
    """
    return flask_app.test_client()  # clean up / reset resources here


@pytest.fixture(autouse=True)
def escape_ansi() -> Callable[[str], str]:
    """Remove ANSI escape sequences from a string.

    Returns
    -------
    Callable[[str], str]
        The escape_ansi function.
    """

    def _escape_ansi(text: str) -> str:
        """Remove ANSI escape sequences from a string.

        Parameters
        ----------
        text : str
            The text to remove ANSI escape sequences from.

        Returns
        -------
        str
            The text with ANSI escape sequences removed.
        """
        if not text:
            return text
        ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", text)

    return _escape_ansi


def _before() -> None:
    """Run before all tests."""
    # tricky if xdist is used


def _after() -> None:
    """Run after all tests."""
    # tricky if xdist is used


# pylint: disable=unused-argument
@pytest.fixture(scope="session", autouse=True)
def before_and_after_tests(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Fixture to run before and after all tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The request object.

    Yields
    ------
    Generator[None, None, None]
        The generator.
    """
    _before()
    yield
    _after()
