Feature: API Testing Scenarios

  Scenario: GraphQL: Execute query on /graphql
    Given the API endpoint '/graphql' is available
    And the following request body is provided:
      """
      {
  "query": "query { test }",
  "variables": {}
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

