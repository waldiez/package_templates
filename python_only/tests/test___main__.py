# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Tests for the __main__ module of my_py_package."""

import sys

import pytest

from my_py_package.__main__ import app as main_app


def test_calling_my_py_package_as_module(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test calling my_py_package as a module.

    just to get full coverage

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        The capsys fixture.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["my_py_package", "--version"]
        main_app()
    captured = capsys.readouterr()
    assert "my-package" in captured.out
