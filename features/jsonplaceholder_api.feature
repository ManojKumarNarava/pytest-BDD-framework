Feature: JSONPlaceholder API validation

    @api @smoke @positive
    Scenario: Retrieve all posts
        When I send a GET request to retrieve all posts
        Then the response status code should be 200
        And the response should be a non-empty list
        And every post should contain valid required fields

    @api @smoke @positive
    Scenario: Retrieve a post by valid ID
        When I send a GET request for post 1
        Then the response status code should be 200
        And the returned post ID should be 1
        And the post response should match the expected schema

    @api @negative
    Scenario: Retrieve a post using an invalid ID
        When I send a GET request for post 00000
        Then the response status code should be 404
        And the invalid resource response should be handled

    @api @smoke @positive
    Scenario: Create a new post
        When I send a POST request with valid post data
        Then the response status code should be 201
        And the response should contain the submitted post
        And the response should contain a generated ID

    @api @positive
    Scenario: Replace a post using PUT
        When I send a PUT request for post 1
        Then the response status code should be 200
        And the response should contain the complete replacement payload

    @api @positive
    Scenario: Partially update a post using PATCH
        When I send a PATCH request for post 1
        Then the response status code should be 200
        And only the requested fields should be updated
        And the unchanged post fields should remain the same

    @api @smoke @positive
    Scenario: Delete a post
        When I send a DELETE request for post 1
        Then the response status code should be 200
        And the delete response should be handled successfully