from pytest_bdd import scenarios, given, then, parsers

from pages.google_page import GooglePage
from utils.assertions import assert_contains


scenarios("../../features/google_search.feature")


@given("the user opens Google")
def open_google(page, base_url):
    GooglePage(page).open(base_url)


@then(
    parsers.parse(
        'the page title should contain "{expected_title}"'
    )
)
def verify_title(page, expected_title):
    assert_contains(
        actual=page.title(),
        expected=expected_title,
    )