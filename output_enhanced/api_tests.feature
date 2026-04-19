Feature: API Testing Scenarios

  Scenario: Positive: GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | tXskPZbIYV |
      | price_min | 74.86410726629627 |
      | price_max | 65.16261766277334 |
      | in_stock | True |
      | limit | 21 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | 123 |
      | price_min | 61.233875129173704 |
      | price_max | 45.80400500541207 |
      | in_stock | False |
      | limit | 10 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | zeyxNoADWT |
      | price_min | not-a-number |
      | price_max | 41.15163711686629 |
      | in_stock | False |
      | limit | 98 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | awxUyhcDez |
      | price_min | 43.395365930612584 |
      | price_max | not-a-number |
      | in_stock | True |
      | limit | 98 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | aXyyBhUzOX |
      | price_min | 83.41071698600668 |
      | price_max | 88.53996140248893 |
      | in_stock | not-a-boolean |
      | limit | 18 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | MydehvipAm |
      | price_min | 5.4893129953908195 |
      | price_max | 6.972589573982157 |
      | in_stock | False |
      | limit | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | None |
      | price_min | 39.943102429126384 |
      | price_max | 68.47596467903321 |
      | in_stock | False |
      | limit | 89 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | RqohkBaNYk |
      | price_min | None |
      | price_max | 79.94041121062308 |
      | in_stock | False |
      | limit | 65 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | BSqXQmInAM |
      | price_min | 79.02171812867876 |
      | price_max | None |
      | in_stock | False |
      | limit | 24 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | NEoogVzdcg |
      | price_min | 1.0755159046052438 |
      | price_max | 79.8132862837229 |
      | in_stock | None |
      | limit | 73 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | JFUjiVMKgO |
      | price_min | 28.965690618496446 |
      | price_max | 55.75575084299337 |
      | in_stock | True |
      | limit | None |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Data-driven: Product search by category - {'params': {'category': 'electronics'}, 'expected_status': 200}
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | electronics |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Data-driven: Product search by category - {'params': {'category': 'clothing'}, 'expected_status': 200}
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | clothing |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Data-driven: Product search by category - {'params': {'category': 'books'}, 'expected_status': 200}
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | books |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Data-driven: Product search by category - {'params': {'category': 'invalid'}, 'expected_status': 400}
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | invalid |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Security: SQL injection attempt
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | '; DROP TABLE products; -- |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Security: SQL Injection in category - GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | '; DROP TABLE users; -- |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: POST /products
    Given the API endpoint '/products' is available
    And the following request body is provided:
      """
      {
  "name": "iPhone 15",
  "description": "Latest smartphone",
  "price": 999.99,
  "category": "electronics",
  "in_stock": true,
  "tags": [
    "smartphone",
    "apple",
    "ios"
  ]
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Security: XSS attempt
    Given the API endpoint '/products' is available
    And the following request body is provided:
      """
      {
  "name": "<script>alert('xss')</script>"
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Security: XSS in request body - POST /products
    Given the API endpoint '/products' is available
    And the following request body is provided:
      """
      {
  "name": "<script>alert('xss')</script>"
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: GET /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | wlLRoRbIqz |
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
      | id | qQoyPjBoeq |
    And the following request body is provided:
      """
      {
  "name": "W3Z",
  "description": "QwF0iBeFvya8Wa2",
  "price": 240.6,
  "category": "clothing",
  "in_stock": false,
  "tags": []
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Missing required parameter 'id' in PUT /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following request body is provided:
      """
      {
  "name": "PKmxv93dq",
  "description": "8EV7l8DrbYPhxGJY5",
  "price": 552.57,
  "category": "electronics",
  "in_stock": true,
  "tags": []
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
  "name": "CRHCOsuSSiR2",
  "description": "ynfRzZKcF",
  "price": 365.21,
  "category": "electronics",
  "in_stock": false,
  "tags": [
    "B0SZ4jNe2nUcO",
    "DRhh5pZLGgkn"
  ]
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Security: XSS in request body - PUT /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following request body is provided:
      """
      {
  "name": "<script>alert('xss')</script>"
}
      """
    When a PUT request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Positive: DELETE /products/{id}
    Given the API endpoint '/products/{id}' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | id | QyCzLrNaQU |
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
  "customer_id": "cust_456",
  "items": [
    {
      "product_id": "prod_3",
      "quantity": 5
    }
  ],
  "shipping_address": {
    "street": "456 Oak Ave",
    "city": "Los Angeles",
    "zip_code": "90210"
  }
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Security: XSS in request body - POST /orders
    Given the API endpoint '/orders' is available
    And the following request body is provided:
      """
      {
  "name": "<script>alert('xss')</script>"
}
      """
    When a POST request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Performance: Products list performance
    Given the API endpoint '/products' is available
    When a GET request is sent to the endpoint
    Then the response status code should be 200

