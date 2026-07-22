from pathlib import Path
from typing import Any

import allure
from pytest_bdd import given, scenarios, then, when
from requests import Response

from src.api.api_client import APIClient


FEATURE_FILE = (
    Path(__file__).resolve().parents[2]
    / "features"
    / "api_posts.feature"
)

scenarios(str(FEATURE_FILE))


@given("the Posts API is available")
def verify_api_client(api_client: APIClient) -> None:
    assert api_client is not None, "API client was not initialized"


@when("I send a GET request for post 1", target_fixture="api_response")
@allure.step("Send GET request for post 1")
def get_post(api_client: APIClient) -> Response:
    response = api_client.get("/posts/1")

    allure.attach(
        response.request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        str(dict(response.request.headers)),
        name="Request Headers",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        response.text,
        name="Response Body",
        attachment_type=allure.attachment_type.JSON,
    )

    return response


@then("the API response status code should be 200")
@allure.step("Validate response status code")
def validate_status_code(api_response: Response) -> None:
    assert api_response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {api_response.status_code}. "
        f"Response: {api_response.text}"
    )


@then("the response content type should be JSON")
@allure.step("Validate response content type")
def validate_content_type(api_response: Response) -> None:
    content_type = api_response.headers.get("Content-Type", "")

    assert "application/json" in content_type.lower(), (
        f"Expected JSON content type, but received: {content_type}"
    )


@then("the response should contain the required post fields")
@allure.step("Validate required response fields")
def validate_required_fields(api_response: Response) -> None:
    response_body: dict[str, Any] = api_response.json()

    required_fields = {
        "userId",
        "id",
        "title",
        "body",
    }

    missing_fields = required_fields - response_body.keys()

    assert not missing_fields, (
        f"Response is missing required fields: {missing_fields}. "
        f"Response: {response_body}"
    )


@then("the returned post ID should be 1")
@allure.step("Validate returned post ID")
def validate_post_id(api_response: Response) -> None:
    response_body = api_response.json()

    assert response_body["id"] == 1, (
        f"Expected post ID 1, but received {response_body['id']}"
    )


@then("the API response time should be less than 5 seconds")
@allure.step("Validate API response time")
def validate_response_time(api_response: Response) -> None:
    response_time = api_response.elapsed.total_seconds()

    assert response_time < 5, (
        f"Expected response time below 5 seconds, "
        f"but received {response_time:.3f} seconds"
    )