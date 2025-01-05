# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Main entry point for my_package."""

import logging
from pathlib import Path

from flask import Flask, Response, request
from paste.translogger import TransLogger  # type: ignore[import-untyped]
from waitress import serve

HERE = Path(__file__).parent
STATIC_ROOT = HERE / "static"
STATIC_ROOT.mkdir(exist_ok=True, parents=True)


def create_app() -> Flask:
    """Create the Flask application.

    Returns
    -------
    Flask
        The Flask application.
    """
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder=str(STATIC_ROOT),
    )

    @app.route("/")
    def root() -> Response:
        """Serve the index.html file.

        Returns
        -------
        Response
            The index.html file.
        """
        return app.send_static_file("index.html")

    @app.route("/health")
    def health() -> Response:
        """Health check endpoint.

        Returns
        -------
        Response
            The health check response.
        """
        return Response("OK", status=200)

    @app.route("/api/v1/hello", methods=["GET"])
    def say_hello() -> Response:
        """Say hello to the user.

        Returns
        -------
        Response
            The hello world response.
        """
        name = request.args.get("name", "World")
        return Response(f"Hello, {name.capitalize()}!", status=200)

    return app


def start(app: Flask, port: int, debug: bool, dev: bool) -> None:
    """Start the application.

    Parameters
    ----------
    app : Flask
        The Flask application.
    port : int
        The port to run the server on.
    debug : bool
        Run the server in debug mode.
    dev : bool
        Run the server in development mode.
    """
    log_level = logging.DEBUG if dev else logging.INFO
    app.config.update(
        {
            "DEBUG": debug,
            "LOG_LEVEL": log_level,
        }
    )
    if dev:
        watchdog_logger = logging.getLogger("watchdog")
        watchdog_logger.setLevel(logging.ERROR)  # skip spam from watchdog
        app.run(host="localhost", port=port, debug=debug, use_reloader=True)
    else:
        waitress_logger = logging.getLogger("waitress")
        waitress_logger.setLevel(log_level)
        app.logger.setLevel(log_level)
        serve(
            TransLogger(
                app,
                setup_console_handler=False,
                logging_level=log_level,
                logger_name="my-package",
            ),
            host="0.0.0.0",
            port=port,
            ident="MyAwesomeApp",
        )
