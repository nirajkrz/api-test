Feature: API Testing Scenarios

  Scenario: Positive: GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 69 |
      | offset | 67 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | not-an-integer |
      | offset | 20 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'offset' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 53 |
      | offset | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'limit' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | None |
      | offset | 90 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'offset' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 33 |
      | offset | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: POST /users
    Given the API endpoint '/users' is available
    And the following request body is provided:
      """
      {
  "name": "kPxuvXUiBU",
  "email": "QyOEvdwqgV",
  "age": 84
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /users/{id}
    Given the API endpoint '/users/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | CCrnXHtAFG |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'id' in GET /users/{id}
    Given the API endpoint '/users/{id}' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'id' in GET /users/{id}
    Given the API endpoint '/users/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | 123 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

