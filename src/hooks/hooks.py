import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info("Starting scenario: %s", scenario.name)


def pytest_bdd_after_scenario(request, feature, scenario):
    logger.info("Finished scenario: %s", scenario.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)