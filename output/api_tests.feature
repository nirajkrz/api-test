Feature: API Testing Scenarios

  Scenario: Positive: GET /latestblock
    Given the API endpoint '/latestblock' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /rawblock/{block_hash}
    Given the API endpoint '/rawblock/{block_hash}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | block_hash | TqslOJidYa |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'block_hash' in GET /rawblock/{block_hash}
    Given the API endpoint '/rawblock/{block_hash}' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'block_hash' in GET /rawblock/{block_hash}
    Given the API endpoint '/rawblock/{block_hash}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | block_hash | 123 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: GET /rawtx/{tx_hash}
    Given the API endpoint '/rawtx/{tx_hash}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | tx_hash | WFFeAjWrpu |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'tx_hash' in GET /rawtx/{tx_hash}
    Given the API endpoint '/rawtx/{tx_hash}' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'tx_hash' in GET /rawtx/{tx_hash}
    Given the API endpoint '/rawtx/{tx_hash}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | tx_hash | 123 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | LCxwhABQcS |
      | limit | 11 |
      | offset | 35 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'bitcoin_address' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | limit | 76 |
      | offset | 92 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'bitcoin_address' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | 123 |
      | limit | 53 |
      | offset | 82 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | wzMKvIPxkh |
      | limit | not-an-integer |
      | offset | 48 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'offset' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | MpfYnDJwkT |
      | limit | 17 |
      | offset | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'limit' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | ziJQxUdrGZ |
      | limit | None |
      | offset | 40 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'offset' in GET /rawaddr/{bitcoin_address}
    Given the API endpoint '/rawaddr/{bitcoin_address}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | bitcoin_address | RjiZaIaALC |
      | limit | 32 |
      | offset | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

