"""End-to-end tests for the Flask app."""

import shutil
import socket
import subprocess  # nosemgrep # nosec
import sys
import time
from contextlib import closing
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, sync_playwright

ROOT_DIR = Path(__file__).parent.parent
DOT_LOCAL = ROOT_DIR / ".local"
DOT_LOCAL.mkdir(exist_ok=True, parents=True)
RECORDINGS_DIR = DOT_LOCAL / "recordings"


def get_available_port() -> int:
    """Get an available port.

    Returns
    -------
    int
        An available port.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as soc:
        soc.bind(("", 0))
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return soc.getsockname()[1]


@pytest.fixture(scope="session", name="app_url")
def app_url_fixture() -> Generator[str, None, None]:
    """Fixture to start the Flask app and return the base URL of the app.

    Yields
    ------
    str
        The base URL of the Flask app.
    """
    port = get_available_port()
    shutil.rmtree(RECORDINGS_DIR, ignore_errors=True)
    # pylint: disable=consider-using-with
    process = subprocess.Popen(  # nosemgrep # nosec
        [sys.executable, "-m", "my_package", "--port", str(port)],
        cwd=ROOT_DIR,
    )
    time.sleep(2)
    yield f"http://localhost:{port}"
    process.terminate()
    process.wait()
    time.sleep(2)
    recordings = list(RECORDINGS_DIR.glob("*.webm"))
    if recordings:
        shutil.move(recordings[0], DOT_LOCAL / "demo.webm")
        convert_webm_to_mp4()


def convert_webm_to_mp4() -> None:
    """Convert the WebM recording to MP4 if ffmpeg is installed."""
    if not shutil.which("ffmpeg"):
        return
    webm_path = DOT_LOCAL / "demo.webm"
    if not webm_path.exists():
        return
    mp4_path = DOT_LOCAL / "demo.mp4"
    cmd_args = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(webm_path),
        str(mp4_path),
    ]
    subprocess.run(cmd_args, check=True)  # nosemgrep # nosec


@pytest.fixture(scope="session", name="browser")
def browser_fixture() -> Generator[Browser, None, None]:
    """Fixture to create a browser instance using Playwright.

    Yields
    ------
    Browser
        A Playwright browser instance.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


def test_home_page(app_url: str, browser: Browser) -> None:
    """Test the homepage of the Flask app.

    Parameters
    ----------
    app_url : str
        The base URL of the Flask app.
    browser : Browser
        A Playwright browser instance.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        reduced_motion="reduce",
        record_video_dir=RECORDINGS_DIR,
        record_video_size={"width": 1280, "height": 720},
    )
    page = context.new_page()
    page.goto(app_url)
    time.sleep(1)
    toggle_theme_button = page.get_by_test_id("toggle-theme-button")
    assert toggle_theme_button
    toggle_theme_button.click()
    time.sleep(1)
    user_input = page.get_by_test_id("user-input")
    assert user_input
    user_input.fill("Alice")
    assert user_input.get_attribute("type") == "text"
    time.sleep(1)
    toggle_visibility_button = page.get_by_test_id(
        "toggle-user-input-visibility-button"
    )
    assert toggle_visibility_button
    toggle_visibility_button.click()
    time.sleep(1)
    assert user_input.get_attribute("type") == "password"
    toggle_visibility_button.click()
    time.sleep(1)
    greet_button = page.get_by_test_id("greet-button")
    assert greet_button
    greet_button.click()
    time.sleep(2)
    greeting = page.get_by_test_id("result")
    assert greeting
    assert greeting.text_content() == "Hello, Alice!"
    context.close()
