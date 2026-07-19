from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from utils.browser_manager import BrowserManager
from utils.config_reader import get_browser, get_timeout, is_headless
from utils.environment_manager import EnvironmentManager
from utils.logger import get_logger


pytest_plugins = ["hooks.hooks"]

logger = get_logger(__name__)

SCREENSHOT_DIRECTORY = Path("screenshots")
SCREENSHOT_DIRECTORY.mkdir(exist_ok=True)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None)
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--env", action="store", default="qa")


@pytest.fixture(scope="session")
def environment(request):
    return EnvironmentManager.validate_environment(
        request.config.getoption("--env")
    )


@pytest.fixture(scope="session")
def base_url(environment):
    return EnvironmentManager.get_application_url(environment)


@pytest.fixture(scope="function")
def page(request):
    browser_name = request.config.getoption("--browser") or get_browser()
    headless = request.config.getoption("--headless") or is_headless()

    with sync_playwright() as playwright:
        browser = BrowserManager.launch_browser(
            playwright,
            browser_name,
            headless,
        )

        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(get_timeout())

        yield page

        report = getattr(request.node, "rep_call", None)

        if report and report.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = request.node.name.replace("/", "_").replace("\\", "_")

            screenshot_path = (
                SCREENSHOT_DIRECTORY
                / f"{safe_name}_{timestamp}.png"
            )

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
                logger.exception("Failure screenshot could not be captured")

        context.close()
        browser.close()