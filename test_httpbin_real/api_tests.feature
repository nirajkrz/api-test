Feature: API Testing Scenarios

  Scenario: Positive: GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | fKPBLhcPPH |
      | param2 | 21 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'param1' in GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | 123 |
      | param2 | 3 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'param2' in GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | WTKmRZSsRa |
      | param2 | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'param1' in GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | None |
      | param2 | 19 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'param2' in GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | XhzFiklkiy |
      | param2 | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Security: SQL Injection in param1 - GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | '; DROP TABLE users; -- |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: POST /post
    Given the API endpoint '/post' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Security: XSS in request body - POST /post
    Given the API endpoint '/post' is available
    And the following request body is provided:
      """
      {
  "name": "<script>alert('xss')</script>"
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: GET /status/200
    Given the API endpoint '/status/200' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

