Feature: API Testing Scenarios

  Scenario: Positive: GET /get
    Given the API endpoint '/get' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | param1 | tPslgxHOQq |
      | param2 | 31 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: POST /post
    Given the API endpoint '/post' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /status/200
    Given the API endpoint '/status/200' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

