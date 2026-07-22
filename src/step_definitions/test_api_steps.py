from pytest_bdd import parsers, scenarios, then, when

from api.endpoints import POSTS_ENDPOINT
from utils.schema_validator import validate_post_schema


scenarios("../../features/jsonplaceholder_api.feature")


# =========================================================
# WHEN STEPS
# =========================================================


@when("I send a GET request to retrieve all posts")
def send_get_request_for_all_posts(
    api_client,
    api_context,
):
    response = api_client.get(POSTS_ENDPOINT)

    api_context["response"] = response


@when(
    parsers.parse(
        "I send a GET request for post {post_id}"
    )
)
def send_get_request_for_post(
    api_client,
    api_context,
    post_id,
):
    response = api_client.get(
        f"{POSTS_ENDPOINT}/{post_id}"
    )

    api_context["response"] = response
    api_context["requested_post_id"] = post_id


@when("I send a POST request with valid post data")
def send_post_request(
    api_client,
    api_context,
    post_payloads,
):
    payload = post_payloads["create_post"]

    response = api_client.post(
        POSTS_ENDPOINT,
        payload,
    )

    api_context["response"] = response
    api_context["submitted_payload"] = payload


@when(
    parsers.parse(
        "I send a PUT request for post {post_id:d}"
    )
)
def send_put_request(
    api_client,
    api_context,
    post_payloads,
    post_id,
):
    payload = post_payloads["put_post"].copy()
    payload["id"] = post_id

    response = api_client.put(
        f"{POSTS_ENDPOINT}/{post_id}",
        payload,
    )

    api_context["response"] = response
    api_context["submitted_payload"] = payload


@when(
    parsers.parse(
        "I send a PATCH request for post {post_id:d}"
    )
)
def send_patch_request(
    api_client,
    api_context,
    post_payloads,
    post_id,
):
    original_response = api_client.get(
        f"{POSTS_ENDPOINT}/{post_id}"
    )

    assert original_response.status_code == 200, (
        "Unable to retrieve the original post before PATCH. "
        f"Response body: {original_response.text}"
    )

    original_post = original_response.json()
    patch_payload = post_payloads["patch_post"]

    response = api_client.patch(
        f"{POSTS_ENDPOINT}/{post_id}",
        patch_payload,
    )

    api_context["response"] = response
    api_context["original_post"] = original_post
    api_context["submitted_payload"] = patch_payload


@when(
    parsers.parse(
        "I send a DELETE request for post {post_id:d}"
    )
)
def send_delete_request(
    api_client,
    api_context,
    post_id,
):
    response = api_client.delete(
        f"{POSTS_ENDPOINT}/{post_id}"
    )

    api_context["response"] = response


# =========================================================
# STATUS VALIDATION
# =========================================================


@then(
    parsers.parse(
        "the response status code should be "
        "{expected_status:d}"
    )
)
def validate_response_status(
    api_context,
    expected_status,
):
    response = api_context["response"]

    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, "
        f"but received {response.status_code}. "
        f"Response body: {response.text}"
    )


# =========================================================
# GET ALL POSTS
# =========================================================


@then("the response should be a non-empty list")
def validate_non_empty_list(api_context):
    response_body = api_context["response"].json()

    assert isinstance(response_body, list), (
        f"Expected response to be a list, but received "
        f"{type(response_body).__name__}"
    )

    assert response_body, (
        "Expected the response list to contain posts, "
        "but it was empty"
    )


@then("every post should contain valid required fields")
def validate_all_post_schemas(api_context):
    posts = api_context["response"].json()

    for index, post in enumerate(posts):
        try:
            validate_post_schema(post)
        except AssertionError as error:
            raise AssertionError(
                f"Post schema validation failed at "
                f"list index {index}: {error}"
            ) from error


# =========================================================
# GET POST BY ID
# =========================================================


@then(
    parsers.parse(
        "the returned post ID should be {expected_id:d}"
    )
)
def validate_returned_post_id(
    api_context,
    expected_id,
):
    post = api_context["response"].json()

    assert post["id"] == expected_id, (
        f"Expected post ID {expected_id}, "
        f"but received {post.get('id')}"
    )


@then("the post response should match the expected schema")
def validate_single_post_schema(api_context):
    post = api_context["response"].json()

    validate_post_schema(post)


# =========================================================
# INVALID RESOURCE
# =========================================================


@then("the invalid resource response should be handled")
def validate_invalid_resource(api_context):
    response = api_context["response"]
    response_body = response.json()

    assert response.status_code == 404

    assert response_body == {}, (
        f"Expected empty JSON object, "
        f"but received {response_body}"
    )


# =========================================================
# POST
# =========================================================


@then("the response should contain the submitted post")
def validate_submitted_post(api_context):
    response_body = api_context["response"].json()
    submitted_payload = api_context["submitted_payload"]

    assert (
        response_body["title"]
        == submitted_payload["title"]
    )

    assert (
        response_body["body"]
        == submitted_payload["body"]
    )

    assert (
        response_body["userId"]
        == submitted_payload["userId"]
    )


@then("the response should contain a generated ID")
def validate_generated_id(api_context):
    response_body = api_context["response"].json()

    assert "id" in response_body, (
        "POST response did not contain a generated ID"
    )

    assert isinstance(response_body["id"], int), (
        f"Generated ID should be integer, but received "
        f"{type(response_body['id']).__name__}"
    )

    assert response_body["id"] > 0


# =========================================================
# PUT
# =========================================================


@then(
    "the response should contain the complete "
    "replacement payload"
)
def validate_complete_put_payload(api_context):
    response_body = api_context["response"].json()
    submitted_payload = api_context["submitted_payload"]

    validate_post_schema(response_body)

    assert response_body == submitted_payload, (
        "PUT response did not match the submitted "
        "replacement payload.\n"
        f"Expected: {submitted_payload}\n"
        f"Actual: {response_body}"
    )


# =========================================================
# PATCH
# =========================================================


@then("only the requested fields should be updated")
def validate_updated_patch_fields(api_context):
    response_body = api_context["response"].json()
    patch_payload = api_context["submitted_payload"]

    for field, expected_value in patch_payload.items():
        assert response_body[field] == expected_value, (
            f"Expected field '{field}' to contain "
            f"'{expected_value}', but received "
            f"'{response_body.get(field)}'"
        )


@then("the unchanged post fields should remain the same")
def validate_unchanged_fields(api_context):
    response_body = api_context["response"].json()
    original_post = api_context["original_post"]
    patch_payload = api_context["submitted_payload"]

    validate_post_schema(response_body)

    for field, original_value in original_post.items():
        if field not in patch_payload:
            assert response_body[field] == original_value, (
                f"Field '{field}' was not included in PATCH, "
                f"but changed from '{original_value}' to "
                f"'{response_body.get(field)}'"
            )


# =========================================================
# DELETE
# =========================================================


@then("the delete response should be handled successfully")
def validate_delete_response(api_context):
    response = api_context["response"]
    response_body = response.json()

    assert response.status_code == 200

    assert response_body == {}, (
        f"Expected empty JSON object after DELETE, "
        f"but received {response_body}"
    )