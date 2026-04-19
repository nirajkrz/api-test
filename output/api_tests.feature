Feature: API Testing Scenarios

  Scenario: Positive: GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 29 |
      | offset | 82 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | not-an-integer |
      | offset | 90 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'offset' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 94 |
      | offset | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'limit' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | None |
      | offset | 41 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'offset' in GET /users
    Given the API endpoint '/users' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 1 |
      | offset | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: POST /users
    Given the API endpoint '/users' is available
    And the following request body is provided:
      """
      {
  "name": "cyAyGXgCzb",
  "email": "IAnAbAolQg",
  "age": 37
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /users/{id}
    Given the API endpoint '/users/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | KMmxlleSiX |
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

