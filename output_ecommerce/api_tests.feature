Feature: API Testing Scenarios

  Scenario: Positive: GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | hgKgyAXYJf |
      | price_min | 45.95581556315406 |
      | price_max | 93.3674349723499 |
      | in_stock | False |
      | limit | 28 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | 123 |
      | price_min | 69.98458036888871 |
      | price_max | 29.945180202921577 |
      | in_stock | True |
      | limit | 77 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | TGbQpdyPbA |
      | price_min | not-a-number |
      | price_max | 49.22062997997775 |
      | in_stock | True |
      | limit | 14 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | drBSswclGq |
      | price_min | 34.51049734730018 |
      | price_max | not-a-number |
      | in_stock | True |
      | limit | 57 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | AZPEsGnxwN |
      | price_min | 82.69386749504731 |
      | price_max | 59.94428347534992 |
      | in_stock | not-a-boolean |
      | limit | 49 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | lSsigOGJNt |
      | price_min | 32.2168425562914 |
      | price_max | 69.9704998086465 |
      | in_stock | False |
      | limit | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | None |
      | price_min | 60.95287384235837 |
      | price_max | 56.20691309336153 |
      | in_stock | True |
      | limit | 69 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | dqvXDZVyFR |
      | price_min | None |
      | price_max | 49.19959087314685 |
      | in_stock | False |
      | limit | 99 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | qXcpWtdqtk |
      | price_min | 9.834673533392525 |
      | price_max | None |
      | in_stock | True |
      | limit | 86 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | yDEJAEksbt |
      | price_min | 84.64912357290648 |
      | price_max | 14.407596074140946 |
      | in_stock | None |
      | limit | 3 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | OklcerIhoa |
      | price_min | 6.670701225879275 |
      | price_max | 40.41186916516473 |
      | in_stock | False |
      | limit | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: POST /products
    Given the API endpoint '/products' is available
    And the following request body is provided:
      """
      {
  "name": "IZbtJiPWjc",
  "description": "DizgiawpPQ",
  "price": 84.91347260624904,
  "category": "HCkkHTWSbm",
  "in_stock": false,
  "tags": null
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Positive: GET /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | tMQMtOzUFz |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'id' in GET /products/{id}
    Given the API endpoint '/products/{id}' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'id' in GET /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | 123 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: PUT /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | YMVsobHIXi |
    And the following request body is provided:
      """
      {
  "name": "elETTwIlzQ",
  "description": "yyGlzZOWMc",
  "price": 37.77756056495784,
  "category": "YCMsiGMBtO",
  "in_stock": true,
  "tags": null
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'id' in PUT /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following request body is provided:
      """
      {
  "name": "TaUapWtFiw",
  "description": "yYVffesdQX",
  "price": 61.29718947170578,
  "category": "AMnvYEeFUh",
  "in_stock": true,
  "tags": null
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'id' in PUT /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | 123 |
    And the following request body is provided:
      """
      {
  "name": "LVothVCSfO",
  "description": "UgGxhIqVhV",
  "price": 95.5392628785824,
  "category": "EGfGiPiqTI",
  "in_stock": true,
  "tags": null
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: DELETE /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | jYPJtlADHG |
    When a DELETE request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'id' in DELETE /products/{id}
    Given the API endpoint '/products/{id}' is available
    When a DELETE request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'id' in DELETE /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | 123 |
    When a DELETE request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: POST /orders
    Given the API endpoint '/orders' is available
    And the following request body is provided:
      """
      {
  "customer_id": "UmGQBsozBn",
  "items": null,
  "shipping_address": null
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

