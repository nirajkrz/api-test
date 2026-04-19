Feature: API Testing Scenarios

  Scenario: Smart Contract: Call name function
    Given the API endpoint '/name' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Smart Contract: Call symbol function
    Given the API endpoint '/symbol' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Smart Contract: Call totalSupply function
    Given the API endpoint '/totalSupply' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Smart Contract: Call balanceOf function
    Given the API endpoint '/balanceOf' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Smart Contract: Call transfer function
    Given the API endpoint '/transfer' is available
    When a POST request is sent to the endpoint
    Then the response status code should be 200

