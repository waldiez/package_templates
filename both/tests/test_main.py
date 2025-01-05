# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Test my_package.app.*."""

from flask.testing import FlaskClient


def test_root(client: FlaskClient) -> None:
    """Test the root endpoint.

    Parameters
    ----------
    client : FlaskClient
        The Flask test client.
    """
    response = client.get("/")
    # the static index.html file might not exist (it comes from the frontend)
    assert response.status_code in {200, 404}
    assert response.content_type == "text/html; charset=utf-8"


def test_health(client: FlaskClient) -> None:
    """Test the health endpoint.

    Parameters
    ----------
    client : FlaskClient
        The Flask test client.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.data == b"OK"


def test_say_hello(client: FlaskClient) -> None:
    """Test the say_hello endpoint.

    Parameters
    ----------
    client : FlaskClient
        The Flask test client.
    """
    response = client.get("/api/v1/hello?name=Alice")
    assert response.status_code == 200
    assert response.data == b"Hello, Alice!"


def test_say_hello_no_name(client: FlaskClient) -> None:
    """Test the say_hello endpoint without a name.

    Parameters
    ----------
    client : FlaskClient
        The Flask test client.
    """
    response = client.get("/api/v1/hello")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"
