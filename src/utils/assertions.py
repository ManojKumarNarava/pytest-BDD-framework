from utils.logger import get_logger


logger = get_logger(__name__)


def assert_contains(
    actual: str,
    expected: str,
    message: str | None = None,
) -> None:

    logger.info(
        "Checking whether '%s' contains '%s'",
        actual,
        expected,
    )

    assert expected in actual, (
        message
        or f"Expected '{actual}' to contain '{expected}'."
    )


def assert_equals(
    actual,
    expected,
    message: str | None = None,
) -> None:

    logger.info(
        "Checking actual value '%s' against expected '%s'",
        actual,
        expected,
    )

    assert actual == expected, (
        message
        or f"Expected '{expected}', but received '{actual}'."
    )


def assert_true(
    condition: bool,
    message: str = "Expected condition to be true.",
) -> None:

    logger.info("Checking that condition is true")
    assert condition, message