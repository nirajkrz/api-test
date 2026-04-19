Feature: API Testing Scenarios

  Scenario: Positive: GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | NmMzDwlBqC |
      | price_min | 67.43343462698002 |
      | price_max | 60.700096832223636 |
      | in_stock | False |
      | limit | 74 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Negative: Invalid data type for parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | 123 |
      | price_min | 94.95161479367098 |
      | price_max | 32.48081183284864 |
      | in_stock | False |
      | limit | 96 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | XgUJZSsmBk |
      | price_min | not-a-number |
      | price_max | 32.13097016264534 |
      | in_stock | False |
      | limit | 99 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | frTkNUrpKB |
      | price_min | 83.23934590554174 |
      | price_max | not-a-number |
      | in_stock | False |
      | limit | 4 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | iPOyHXQtIt |
      | price_min | 17.37967435041326 |
      | price_max | 76.67143209802808 |
      | in_stock | not-a-boolean |
      | limit | 51 |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Negative: Invalid data type for parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | eiLkjNRPAw |
      | price_min | 68.28708079843288 |
      | price_max | 29.336821605758065 |
      | in_stock | False |
      | limit | not-an-integer |
    When a GET request is sent to the endpoint
    Then the response status code should be 400

  Scenario: Edge: Null value for optional parameter 'category' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | None |
      | price_min | 78.14129336724712 |
      | price_max | 60.748735060763295 |
      | in_stock | False |
      | limit | 26 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_min' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | suzYHQKBdd |
      | price_min | None |
      | price_max | 62.20237920258134 |
      | in_stock | False |
      | limit | 13 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'price_max' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | KWJwtZuMGh |
      | price_min | 76.84202623187527 |
      | price_max | None |
      | in_stock | False |
      | limit | 43 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'in_stock' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | MbJbWMJteQ |
      | price_min | 57.44984837058717 |
      | price_max | 97.75133680192509 |
      | in_stock | None |
      | limit | 45 |
    When a GET request is sent to the endpoint
    Then the response status code should be 200

  Scenario: Edge: Null value for optional parameter 'limit' in GET /products
    Given the API endpoint '/products' is available
    And the following query parameters are provided:
      | Parameter | Value |
      | category | SkyEBCThJB |
      | price_min | 9.887470808418097 |
      | price_max | 17.47925566826751 |
      | in_stock | False |
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
  "name": "T-shirt",
  "description": "Cotton t-shirt",
  "price": 19.99,
  "category": "clothing",
  "in_stock": false,
  "tags": [
    "casual",
    "cotton"
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
      | id | GRzFEAROsw |
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
      | id | MjbJRFCTyK |
    And the following request body is provided:
      """
      {
  "name": "dOe6GTGmfmEg3AAY0Z",
  "description": "Pve7b2n4zg09XZnkXB",
  "price": 138.0,
  "category": "electronics",
  "in_stock": true,
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
  "name": "lFd1S7thd0",
  "description": "4n5P0WrU9YVUWhLS",
  "price": 5.3,
  "category": "books",
  "in_stock": true,
  "tags": [
    "ddlnCxO2PS2qqA",
    "twCANyd",
    "",
    "83kqxebe5aq7fEZvS",
    "B9ycr8kjXv2HM"
  ]
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
  "name": "EfU5",
  "description": "uhBQlasrwTXvue",
  "price": 878.42,
  "category": "books",
  "in_stock": false,
  "tags": [
    "NZ",
    "",
    "Hw4OsBmr",
    "DRIhp",
    "lG45q"
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
      | id | YZtvQnFEer |
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
  "customer_id": "cust_123",
  "items": [
    {
      "product_id": "prod_1",
      "quantity": 2
    },
    {
      "product_id": "prod_2",
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "zip_code": "10001"
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

