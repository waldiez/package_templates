# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""CLI management for my_package."""

import os
import sys

import typer

from ._version import __version__
from .main import create_app, start

ENV_PREFIX = "MY_PACKAGE_"


def get_default_port() -> int:
    """Get the default port.

    Returns
    -------
    int
        The default port
    """
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port") + 1
        if port_index < len(sys.argv):
            try:
                port = int(sys.argv[port_index])
                os.environ[f"{ENV_PREFIX}PORT"] = str(port)
                return port
            except ValueError:
                pass
    try:
        return int(os.environ.get(f"{ENV_PREFIX}PORT", "8000"))
    except ValueError:
        return 8000


app = typer.Typer(
    name="my-package",
    help="A template for creating Python packages.",
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    add_completion=False,
    no_args_is_help=False,
    invoke_without_command=True,
    add_help_option=True,
    pretty_exceptions_enable=False,
    epilog=("Use 'my-package <command> --help' for more information."),
)


# pylint: disable=missing-param-doc,missing-return-doc,missing-raises-doc
@app.command()
def run(
    port: int = typer.Option(
        default=get_default_port(),
        help="The port to run the server on",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Run the server in debug mode",
    ),
    dev: bool = typer.Option(
        False,
        "--dev",
        help="Run the server in development mode",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show the version",
    ),
) -> None:
    """Run the application."""
    if version:
        typer.echo(f"my-package {__version__}")
        raise typer.Exit()
    flask_app = create_app()
    try:
        start(app=flask_app, port=port, debug=debug, dev=dev)
    except BaseException as error:  # pylint: disable=broad-except
        typer.echo(error)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
