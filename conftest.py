from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

import allure
import pytest
import pytest_html
from playwright.sync_api import sync_playwright

from utils.browser_manager import BrowserManager
from utils.config_reader import (
    get_browser,
    get_timeout,
    is_headless,
)
from utils.environment_manager import EnvironmentManager
from utils.logger import get_logger


pytest_plugins = ["hooks.hooks"]

logger = get_logger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parent

REPORT_DIRECTORY = PROJECT_ROOT / "reports"
SCREENSHOT_DIRECTORY = PROJECT_ROOT / "screenshots"
TRACE_DIRECTORY = PROJECT_ROOT / "traces"
VIDEO_DIRECTORY = PROJECT_ROOT / "videos"
ALLURE_RESULTS_DIRECTORY = PROJECT_ROOT / "allure-results"

for directory in (
    REPORT_DIRECTORY,
    SCREENSHOT_DIRECTORY,
    TRACE_DIRECTORY,
    VIDEO_DIRECTORY,
    ALLURE_RESULTS_DIRECTORY,
):
    directory.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser: chromium, firefox or webkit",
    )

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser without visible UI",
    )

    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment: qa, uat or prod",
    )

    parser.addoption(
        "--record-video",
        action="store_true",
        default=False,
        help="Record video for every test",
    )

    parser.addoption(
    "--playwright-trace",
    action="store_true",
    default=False,
    help="Record Playwright trace for every test",
)


@pytest.fixture(scope="session")
def environment(request):
    selected_environment = request.config.getoption("--env")

    return EnvironmentManager.validate_environment(
        selected_environment
    )


@pytest.fixture(scope="session")
def base_url(environment):
    return EnvironmentManager.get_application_url(environment)


@pytest.fixture(scope="function")
def page(request):
    browser_name = (
        request.config.getoption("--browser")
        or get_browser()
    )

    headless = (
        request.config.getoption("--headless")
        or is_headless()
    )

    record_video = request.config.getoption("--record-video")
    record_trace = request.config.getoption("--playwright-trace")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_test_name = sanitize_filename(request.node.name)

    screenshot_path = (
        SCREENSHOT_DIRECTORY
        / f"{safe_test_name}_{timestamp}.png"
    )

    trace_path = (
        TRACE_DIRECTORY
        / f"{safe_test_name}_{timestamp}.zip"
    )

    video_path = (
        VIDEO_DIRECTORY
        / f"{safe_test_name}_{timestamp}.webm"
    )

    with sync_playwright() as playwright:
        browser = BrowserManager.launch_browser(
            playwright,
            browser_name,
            headless,
        )

        context_options = {
            "viewport": {
                "width": 1440,
                "height": 900,
            }
        }

        if record_video:
            context_options["record_video_dir"] = str(
                VIDEO_DIRECTORY
            )

            context_options["record_video_size"] = {
                "width": 1280,
                "height": 720,
            }

        context = browser.new_context(**context_options)

        if record_trace:
            context.tracing.start(
                screenshots=True,
                snapshots=True,
                sources=True,
                title=request.node.name,
            )

        browser_page = context.new_page()
        browser_page.set_default_timeout(get_timeout())

        logger.info(
            "Test started | browser=%s | headless=%s | env=%s",
            browser_name,
            headless,
            request.config.getoption("--env"),
        )

        yield browser_page

        report = getattr(request.node, "rep_call", None)
        test_failed = bool(report and report.failed)

        if test_failed:
            capture_failure_screenshot(
                browser_page,
                screenshot_path,
            )

            request.node.failure_screenshot_path = screenshot_path

            attach_screenshot_to_allure(screenshot_path)
            attach_screenshot_to_html(
                request,
                screenshot_path,
            )

        if record_trace:
            save_trace(
                context=context,
                trace_path=trace_path,
                keep_trace=test_failed,
            )

            if test_failed and trace_path.exists():
                request.node.failure_trace_path = trace_path
                attach_trace_to_allure(trace_path)

        raw_video_path = None

        if record_video and browser_page.video:
            try:
                raw_video_path = browser_page.video.path()
            except Exception:
                logger.exception(
                    "Could not retrieve temporary video path"
                )

        context.close()

        if record_video and raw_video_path:
            save_or_delete_video(
                raw_video_path=Path(raw_video_path),
                final_video_path=video_path,
                keep_video=test_failed,
            )

            if test_failed and video_path.exists():
                request.node.failure_video_path = video_path
                attach_video_to_allure(video_path)

        browser.close()

        logger.info(
            "Test completed: %s",
            request.node.name,
        )


def sanitize_filename(value: str) -> str:
    """
    Convert a pytest test name into a Windows-safe filename.
    """

    invalid_characters = '<>:"/\\|?*'

    sanitized_value = value

    for character in invalid_characters:
        sanitized_value = sanitized_value.replace(
            character,
            "_",
        )

    return sanitized_value.replace(" ", "_")


def capture_failure_screenshot(page, screenshot_path: Path):
    try:
        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        logger.error(
            "Failure screenshot saved: %s",
            screenshot_path.resolve(),
        )

    except Exception:
        logger.exception(
            "Failure screenshot could not be captured"
        )


def save_trace(
    context,
    trace_path: Path,
    keep_trace: bool,
):
    try:
        if keep_trace:
            context.tracing.stop(
                path=str(trace_path)
            )

            logger.error(
                "Failure trace saved: %s",
                trace_path.resolve(),
            )
        else:
            context.tracing.stop()

            logger.info(
                "Trace discarded because the test passed"
            )

    except Exception:
        logger.exception(
            "Playwright trace could not be processed"
        )


def save_or_delete_video(
    raw_video_path: Path,
    final_video_path: Path,
    keep_video: bool,
):
    try:
        if not raw_video_path.exists():
            logger.warning(
                "Temporary video file was not found: %s",
                raw_video_path,
            )
            return

        if keep_video:
            raw_video_path.replace(final_video_path)

            logger.error(
                "Failure video saved: %s",
                final_video_path.resolve(),
            )
        else:
            raw_video_path.unlink(missing_ok=True)

            logger.info(
                "Video discarded because the test passed"
            )

    except Exception:
        logger.exception(
            "Video file could not be processed"
        )


def attach_screenshot_to_allure(
    screenshot_path: Path,
):
    if not screenshot_path.exists():
        return

    try:
        allure.attach.file(
            str(screenshot_path),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    except Exception:
        logger.exception(
            "Screenshot could not be attached to Allure"
        )


def attach_trace_to_allure(trace_path: Path):
    if not trace_path.exists():
        return

    try:
        allure.attach.file(
            str(trace_path),
            name="Playwright Trace",
            attachment_type="application/zip",
            extension="zip",
        )

    except Exception:
        logger.exception(
            "Trace could not be attached to Allure"
        )


def attach_video_to_allure(video_path: Path):
    if not video_path.exists():
        return

    try:
        allure.attach.file(
            str(video_path),
            name="Execution Video",
            attachment_type="video/webm",
            extension="webm",
        )

    except Exception:
        logger.exception(
            "Video could not be attached to Allure"
        )


def attach_screenshot_to_html(
    request,
    screenshot_path: Path,
):
    """
    Add the screenshot as a base64 image to pytest-html.

    Because fixture teardown occurs after the normal call-stage report,
    this modifies the stored report object directly.
    """

    report = getattr(request.node, "rep_call", None)

    if report is None or not screenshot_path.exists():
        return

    try:
        screenshot_bytes = screenshot_path.read_bytes()
        encoded_image = base64.b64encode(
            screenshot_bytes
        ).decode("utf-8")

        extras = getattr(report, "extras", [])

        extras.append(
            pytest_html.extras.png(
                encoded_image,
                name="Failure Screenshot",
            )
        )

        report.extras = extras

    except Exception:
        logger.exception(
            "Screenshot could not be attached to HTML report"
        )