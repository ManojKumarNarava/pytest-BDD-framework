Feature: JSONPlaceholder Posts API

  Scenario: Retrieve an existing post
    Given the Posts API is available
    When I send a GET request for post 1
    Then the API response status code should be 200
    And the response content type should be JSON
    And the response should contain the required post fields
    And the returned post ID should be 1
    And the API response time should be less than 5 seconds