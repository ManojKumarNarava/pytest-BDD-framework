from __future__ import annotations

import base64
from pathlib import Path

import allure
import pytest
import pytest_html

from utils.logger import get_logger


logger = get_logger(__name__)


def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info("Starting scenario: %s", scenario.name)


def pytest_bdd_after_scenario(request, feature, scenario):
    logger.info("Finished scenario: %s", scenario.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Stores setup, call and teardown reports on the test node.

    Examples:
        item.rep_setup
        item.rep_call
        item.rep_teardown
    """

    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)

    if report.when != "call":
        return

    screenshot_path = getattr(item, "failure_screenshot_path", None)
    trace_path = getattr(item, "failure_trace_path", None)
    video_path = getattr(item, "failure_video_path", None)

    # Attach screenshot to pytest-html report
    if screenshot_path and Path(screenshot_path).exists():
        try:
            screenshot_bytes = Path(screenshot_path).read_bytes()
            encoded_image = base64.b64encode(screenshot_bytes).decode("utf-8")

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
                "Could not attach screenshot to HTML report"
            )

    # Attach screenshot to Allure
    if screenshot_path and Path(screenshot_path).exists():
        try:
            allure.attach.file(
                str(screenshot_path),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            logger.exception(
                "Could not attach screenshot to Allure"
            )

    # Attach trace to Allure
    if trace_path and Path(trace_path).exists():
        try:
            allure.attach.file(
                str(trace_path),
                name="Playwright Trace",
                attachment_type="application/zip",
                extension="zip",
            )
        except Exception:
            logger.exception(
                "Could not attach trace to Allure"
            )

    # Attach video to Allure
    if video_path and Path(video_path).exists():
        try:
            allure.attach.file(
                str(video_path),
                name="Execution Video",
                attachment_type="video/webm",
                extension="webm",
            )
        except Exception:
            logger.exception(
                "Could not attach video to Allure"
            )


def pytest_html_report_title(report):
    report.title = "Playwright Python BDD Automation Report"