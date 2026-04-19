Feature: API Testing Scenarios

  Scenario: Positive: GET /users
    Given the API endpoint '/users' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: POST /users
    Given the API endpoint '/users' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /users/123
    Given the API endpoint '/users/123' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

