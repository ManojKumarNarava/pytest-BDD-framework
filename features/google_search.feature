Feature: Google Search

  Scenario: Verify Google title
    Given the user opens Google
    Then the page title should contain "Google"