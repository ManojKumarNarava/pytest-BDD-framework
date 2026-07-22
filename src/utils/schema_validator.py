def validate_post_schema(post):
    required_fields = {"id", "userId", "title", "body"}

    missing_fields = required_fields - post.keys()
    assert not missing_fields, f"Missing fields: {missing_fields}"

    assert isinstance(post["id"], int), (
        f"Expected id to be int, but received "
        f"{type(post['id']).__name__}"
    )

    assert isinstance(post["userId"], int), (
        f"Expected userId to be int, but received "
        f"{type(post['userId']).__name__}"
    )

    assert isinstance(post["title"], str), (
        f"Expected title to be str, but received "
        f"{type(post['title']).__name__}"
    )

    assert isinstance(post["body"], str), (
        f"Expected body to be str, but received "
        f"{type(post['body']).__name__}"
    )