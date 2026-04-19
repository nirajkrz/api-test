# 🚀 Professional API Testing Framework

A comprehensive, enterprise-grade API testing tool that dynamically generates and executes test suites from various contract specifications. Supports REST APIs, GraphQL, smart contracts, and more with advanced features like authentication, parallel execution, schema validation, and performance testing.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-9+-yellow.svg)](#testing)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Supported Formats](#-supported-formats)
- [Test Types](#-test-types)
- [Reporting](#-reporting)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔧 Core Capabilities
- **Multi-Format Support**: OpenAPI/Swagger, GraphQL, Smart Contract ABIs, Postman Collections
- **Dynamic Test Generation**: Automatic creation of positive, negative, edge, security, and performance tests
- **Real API Execution**: Actual HTTP requests with response validation
- **Parallel Execution**: Multi-threaded test execution for performance
- **Schema Validation**: JSON Schema validation for response structures

### 🔐 Authentication & Security
- **Multiple Auth Types**: Basic, Bearer Token, API Key, OAuth2
- **Security Testing**: SQL injection, XSS, and custom security scenarios
- **Session Management**: Persistent HTTP sessions with connection pooling
- **Request/Response Headers**: Full header capture and validation

### 🌍 Environment Management
- **Multi-Environment**: Dev, staging, production configurations
- **Dynamic Configuration**: Environment-specific settings and variables
- **Configuration Files**: JSON/YAML-based configuration management

### ⚡ Performance & Reliability
- **Load Testing**: Performance test scenarios with metrics
- **Retry Mechanisms**: Automatic retries with exponential backoff
- **Response Time Profiling**: Detailed timing and performance metrics
- **Error Handling**: Comprehensive error handling and logging

### 📊 Advanced Testing
- **Test Filtering**: Filter by type, tags, or custom criteria
- **Data-Driven Testing**: Test scenarios with multiple data sets
- **Custom Assertions**: Extensible validation framework
- **Gherkin Generation**: Human-readable test scenarios

### 🎯 Developer Experience
- **Verbose Logging**: Detailed execution logs and debugging
- **Real-time Progress**: Console output with PASS/FAIL indicators
- **CI/CD Integration**: Command-line interface for automation
- **Extensible Architecture**: Plugin-ready design for customization

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Professional API Testing Framework           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Input Parser│  │Test Generator│  │Test Executor│  │Result   │ │
│  │             │  │             │  │             │  │Publisher│ │
│  │ • OpenAPI   │  │ • Positive  │  │ • HTTP      │  │         │ │
│  │ • GraphQL   │  │ • Negative  │  │ • Parallel  │  │ • HTML  │ │
│  │ • ABI       │  │ • Edge      │  │ • Auth      │  │ • JSON  │ │
│  │ • Postman   │  │ • Security  │  │ • Schema    │  │ • XML   │ │
│  │ • Auto-detect│  │ • Performance│  │ • Retry     │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │Environment  │  │Auth Config  │  │Test Filters │  │Logging  │ │
│  │Management   │  │             │  │             │  │& Debug  │ │
│  │             │  │ • Basic     │  │ • By Type   │  │         │ │
│  │ • Dev/Staging│  │ • Bearer    │  │ • By Tags  │  │ • File  │ │
│  │ • Prod       │  │ • API Key   │  │ • Custom    │  │ • Console│ │
│  │ • Dynamic    │  │ • OAuth2    │  │             │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

- **Input Parser**: Detects and parses various API contract formats
- **Test Generator**: Creates comprehensive test suites with multiple scenarios
- **Test Executor**: Executes tests with authentication, retry, and validation
- **Result Publisher**: Generates detailed reports in multiple formats
- **Configuration**: Environment and authentication management
- **Logging**: Comprehensive logging and debugging capabilities

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from Source
```bash
# Clone the repository
git clone https://github.com/your-username/api-testing-framework.git
cd api-testing-framework

# Install dependencies
pip install -r requirements.txt

# Optional: Install additional packages for enhanced features
pip install jsonschema urllib3
```

### Requirements
```
requests>=2.25.0
PyYAML>=5.4.0
pytest>=6.0.0
jinja2>=2.11.0
jsonschema>=3.2.0
urllib3>=1.26.0
```

## 🚀 Quick Start

### Basic Usage
```bash
# Test an OpenAPI specification
python src/main.py --contract examples/swagger.yaml --base-url https://api.example.com

# Test with environment configuration
python src/main.py --contract api.yaml --env staging --auth auth.json

# Run specific test types with parallel execution
python src/main.py --contract api.yaml --filter positive,security --parallel 4
```

> Note: `--base-url` is used by the current implementation to construct each request URL. If you do not pass `--base-url`, the tool will fall back to the selected environment configuration from `environments.json` or the default `http://localhost:8000`.
>
> The current parser does not automatically extract the OpenAPI `servers` list from Swagger/OpenAPI definitions, so `--base-url` or an environment-specific base URL is still needed unless your contract paths already contain full URLs.

### Sample Output
```
2026-04-19 21:05:24,748 - INFO - Starting API testing with contract: api.yaml
2026-04-19 21:05:24,748 - INFO - Environment: staging, Base URL: https://api-staging.example.com
2026-04-19 21:05:24,771 - INFO - Generated 15 test cases after filtering
2026-04-19 21:05:24,772 - INFO - Executing 15 tests against: https://api-staging.example.com

============================================================
EXECUTING TEST CASES
============================================================

[1/15] Executing: Positive: GET /users
Result: ✓ PASS

[2/15] Executing: Security: SQL Injection in user_id - GET /users/{id}
Result: ✗ FAIL
  Expected: 400, Got: 200

============================================================
SUMMARY: 12/15 tests passed
============================================================
```

## � Distribution & Pipeline Integration

Make the tool easy to share and run in CI/CD or Lightspeed-style pipelines with one of these approaches:

### 1. Install and run directly
- Clone or checkout the repository
- Create a virtual environment
- Install dependencies with `pip install -r requirements.txt`

Example:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py --contract examples/swagger.yaml --env staging --auth auth.json --output-dir output
```

### 2. Use a Docker container
Build a reusable container image and run test commands inside it.
```bash
docker build -t api-test .
docker run --rm \
  -v "$PWD/examples":/app/examples \
  -v "$PWD/auth_config.json":/app/auth_config.json \
  -v "$PWD/environments.json":/app/environments.json \
  api-test \
  --contract examples/swagger.yaml \
  --env staging \
  --auth auth_config.json \
  --output-dir /app/output
```

### 3. Use secure secrets, not checked-in credentials
- Store bearer tokens, client secrets, and API keys in your pipeline secret store
- Mount auth config or inject values as environment variables
- Keep `auth.json` out of source control

### Lightspeed / CI pipeline pattern
Use the same CLI in pipeline steps. Keep auth and environment config separate from test metadata.

Example pipeline step:
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4

  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'

  - name: Install dependencies
    run: pip install -r requirements.txt

  - name: Run API tests
    run: |
      python src/main.py \
        --contract examples/swagger.yaml \
        --env staging \
        --auth auth.json \
        --metadata examples/ecommerce_metadata.yaml \
        --output-dir output

  - name: Upload results
    uses: actions/upload-artifact@v4
    with:
      name: api-test-results
      path: output/
```

### Best practices for pipeline use
- Keep environment-specific values in `environments.json`
- Keep credentials in pipeline secret storage
- Use `--auth` to load secure credentials at runtime
- Mount secrets into containers or use secure file injection
- Publish `output/results.json` and reports as pipeline artifacts

## �📖 Usage

### Command Line Options

```
Usage: python src/main.py [OPTIONS]

Required Arguments:
  --contract CONTRACT      Path to API contract/specification file

Optional Arguments:
  --metadata METADATA [METADATA ...]  Path(s) to metadata/configuration file(s) (YAML)
  --base-url BASE_URL      Base URL of the API (overrides environment config)
  --env ENV               Environment configuration (default: default)
  --output-dir DIR         Output directory for results (default: output)
  --contract-type TYPE     Force contract type (openapi, abi, graphql, postman, auto)

Notes:
  - You can supply multiple metadata files with `--metadata file1.yaml file2.yaml`.
  - Metadata files are merged in order, so later files can override values from earlier files.
  - If `--base-url` is omitted, the tool will use the selected environment's `base_url` from `environments.json`.
  - If no environment setting is available, the tool defaults to `http://localhost:8000`.
  - OpenAPI `servers` lists are not currently auto-parsed, so providing a base URL is the safest option.

Authentication:
  --auth AUTH_FILE        Authentication configuration file

Execution Control:
  --parallel N            Number of parallel workers (default: 1)
  --retry N              Number of retries for failed requests (default: 0)
  --filter TYPES          Filter tests by type (comma-separated)
  --tags TAGS            Filter tests by tags (comma-separated)

Validation:
  --validate-schema       Enable JSON schema validation
  --verbose, -v          Enable verbose logging

Reporting:
  --generate-report       Generate HTML/JSON reports (default: true)
```

### Authentication Setup

Use the `--auth` flag to keep credentials separate from contract definitions and environment settings.

- `--auth auth.json` loads authentication details from a secured file
- Keep auth config out of source control and store secrets in Vault or CI/CD secrets
- Combine with `--env staging` to separate environment values from credentials

Example:
```bash
python src/main.py --contract examples/swagger.yaml --env staging --auth auth.json
```

Supported auth types:
- `bearer` tokens
- `basic` authentication
- `api_key`
- `oauth2`

### Example: separate auth and environment config
```bash
# Environment file contains base URL, timeout, retry
python src/main.py --contract examples/swagger.yaml --env staging --auth auth.json
```

### Environment Variables
```bash
export API_TEST_BASE_URL="https://api.example.com"
export API_TEST_AUTH_TOKEN="your-token"
export API_TEST_ENV="staging"
```

## ⚙️ Configuration

### Environment Configuration (`environments.json`)
```json
{
  "dev": {
    "base_url": "http://localhost:3000",
    "timeout": 30,
    "retries": 3
  },
  "staging": {
    "base_url": "https://api-staging.example.com",
    "timeout": 60,
    "retries": 2
  },
  "prod": {
    "base_url": "https://api.example.com",
    "timeout": 30,
    "retries": 1
  }
}
```

### Authentication Configuration (`auth.json`)

Use separate auth configuration files for sensitive credentials. This keeps auth details isolated from contract definitions and environment settings.

Bearer token example:
```json
{
  "type": "bearer",
  "token": "your-jwt-token"
}
```

Basic authentication example:
```json
{
  "type": "basic",
  "username": "user",
  "password": "pass"
}
```

API Key example:
```json
{
  "type": "api_key",
  "location": "header",
  "header_name": "X-API-Key",
  "api_key": "your-api-key"
}
```

OAuth2 example:
```json
{
  "type": "oauth2",
  "token_url": "https://auth.example.com/oauth/token",
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "scopes": ["read", "write"]
}
```

### Metadata Configuration (`metadata.yaml`)
```yaml
environment:
  base_url: "https://api.example.com"
  timeout: 30

test_data:
  users:
    - name: "John Doe"
      email: "john@example.com"
    - name: "Jane Smith"
      email: "jane@example.com"

custom_assertions:
  - endpoint: "/users"
    method: "GET"
    assertions:
      - type: "status_code"
        expected: 200
      - type: "response_time"
        max_ms: 1000

# Note: response-time and other custom assertions are only applied when configured explicitly.
# The tool does not enforce default timing limits unless you define them in metadata.

data_driven_scenarios:
  - name: "User search by status"
    endpoint: "/users"
    method: "GET"
    test_cases:
      - params: { "status": "active" }
        expected_status: 200
      - params: { "status": "inactive" }
        expected_status: 200

performance_tests:
  - name: "Users API load test"
    endpoint: "/users"
    method: "GET"
    concurrent_users: 10
    duration_seconds: 30
    assertions:
      - type: "response_time_p95"
        max_ms: 500
      - type: "error_rate"
        max_percent: 1

security_tests:
  - name: "SQL injection attempt"
    endpoint: "/users"
    method: "GET"
    params: { "id": "'; DROP TABLE users; --" }
    expected_status: 400
```

## Minimal Metadata Workflow

When full API contract details are unavailable, start with only the information you do have:
- HTTP method and endpoint path
- sample request payload or query parameters
- expected response status
- response keys or basic output shape

Keep auth and environment configuration separate from payload/test metadata by using `auth.json` and `environments.json`.

### Minimal metadata example
```yaml
minimal_endpoints:
  - path: /orders
    method: POST
    request:
      body:
        customer_id: 123
        amount: 100.0
    expected:
      status_code: 201
      response_keys:
        - order_id
        - status
```

### How to use minimal metadata
1. Create a minimal metadata file with only known fields.
2. Run the tool with `--auth` and `--env` to keep credentials and environment separate.
3. Capture actual API responses and use them to refine the metadata.
4. Add schema and assertion details over time as more API behavior becomes known.

Example command:
```bash
python src/main.py \
  --contract examples/swagger.yaml \
  --metadata examples/minimal_metadata.yaml examples/extra_metadata.yaml \
  --env staging \
  --auth auth.json
```

### Recommended iteration process
- Start with minimal metadata when only request/response examples exist
- Supplement with real request/response examples as you discover them
- Keep auth and environment config separate from test metadata
- Re-run tests after each update to refine assertions
- Expand minimal metadata into a fuller contract as the API becomes better defined

## � Supplying richer metadata and business rules

### Provide richer metadata and real request/response examples
Use `metadata.yaml` to describe real API behavior, not just schema.

Example:
```yaml
request_examples:
  - endpoint: /orders
    method: POST
    description: "Create order with customer details"
    headers:
      Content-Type: application/json
    body:
      customer_id: 123
      items:
        - sku: "ABC123"
          quantity: 2
      payment_method: "card"
    expected_response:
      status_code: 201
      body:
        order_id: 1001
        status: "confirmed"
        total_amount: 234.56

response_examples:
  - endpoint: /orders/{order_id}
    method: GET
    expected_response:
      status_code: 200
      body:
        order_id: 1001
        status: "confirmed"
        customer_id: 123
        items:
          - sku: "ABC123"
            quantity: 2
```

This lets the tool generate more meaningful tests and helps you refine validation rules over time.

### Add custom assertions and business rules
Define endpoint-level assertions in metadata to capture business behavior:

```yaml
custom_assertions:
  - endpoint: /orders
    method: POST
    assertions:
      - type: status_code
        expected: 201
      - type: response_body_contains
        path: status
        expected: confirmed
      - type: response_body_value
        path: total_amount
        comparator: ">="
        expected: 0
      - type: response_body_value
        path: customer_id
        comparator: ">"
        expected: 0
```

For business-rule tests, define scenarios such as:
- an order must not be created with a negative amount
- VIP customers receive `priority` status
- a refund request must include a valid transaction ID

If the current implementation does not yet evaluate every assertion type, use these definitions as a design pattern to extend `TestGenerator` and `TestExecutor`.

### Extend `TestGenerator` with domain-aware scenarios
Add domain-level metadata sections that describe business rules and scenario variants:

```yaml
business_rules:
  - name: "VIP order discount"
    endpoint: /orders
    method: POST
    payload:
      customer_type: "VIP"
      items:
        - sku: "ABC123"
          quantity: 1
    expected:
      status_code: 201
      body:
        discount_applied: true

  - name: "Reject invalid payment type"
    endpoint: /orders
    method: POST
    payload:
      payment_method: "cash"
    expected:
      status_code: 400
```

Then extend `src/test_generator.py`:
- Add a new metadata handler such as `_generate_business_rules_tests`
- Convert `business_rules` into test cases with explicit payload, headers, and expected response
- Add domain-aware naming and tags for each generated scenario

Example change in `TestGenerator.generate_test_cases()`:
```python
if self.metadata.get('business_rules'):
    test_cases.extend(self._generate_business_rules_tests())
```

Example handler:
```python
def _generate_business_rules_tests(self):
    tests = []
    for rule in self.metadata.get('business_rules', []):
        tests.append({
            'name': rule['name'],
            'type': 'business_rule',
            'endpoint': rule['endpoint'],
            'method': rule['method'],
            'requestBody': {'content': {'application/json': {'example': rule['payload']}}},
            'expected': rule['expected'],
            'tags': ['business_rule']
        })
    return tests
```

This pattern creates stronger test coverage for domain-specific requirements and makes the suite more useful in production.

## �📄 Supported Formats

### OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /users:
    get:
      responses:
        '200':
          description: Success
```

### GraphQL Schema
```graphql
type Query {
  users: [User!]!
  user(id: ID!): User
}

type User {
  id: ID!
  name: String!
  email: String!
}
```

### Smart Contract ABI
```json
[
  {
    "constant": true,
    "inputs": [],
    "name": "name",
    "outputs": [{"name": "", "type": "string"}],
    "type": "function"
  }
]
```

### Postman Collection
```json
{
  "info": {"name": "API Collection"},
  "item": [
    {
      "name": "Get Users",
      "request": {
        "method": "GET",
        "url": {"raw": "{{base_url}}/users"}
      }
    }
  ]
}
```

## 🧪 Test Types

### Positive Tests
- Valid requests with expected successful responses
- Proper data types and required fields
- Expected status codes (200, 201, etc.)

### Negative Tests
- Missing required parameters
- Invalid data types
- Malformed requests
- Boundary value violations

### Edge Cases
- Null/empty optional parameters
- Maximum/minimum values
- Special characters
- Unicode handling

### Security Tests
- SQL injection attempts
- XSS payloads
- Authentication bypass attempts
- Input validation bypass

### Data-Driven Tests
- Multiple test scenarios with different data sets
- Parameterized testing
- Scenario-based validation

### Performance Tests
- Response time validation
- Concurrent user simulation
- Load testing scenarios
- Throughput measurement

## 📊 Reporting

### HTML Report
Interactive web-based report with:
- Test execution summary
- Detailed test results
- Response time charts
- Assertion details
- Request/response headers

### JSON Report
Machine-readable format containing:
- Complete test results
- Performance metrics
- Assertion outcomes
- Execution metadata

### Console Output
Real-time progress with:
- Test execution status (PASS/FAIL)
- Expected vs actual results
- Response times
- Error details

## 💡 Examples

### Basic REST API Testing
```bash
python src/main.py \
  --contract examples/swagger.yaml \
  --base-url https://jsonplaceholder.typicode.com \
  --output-dir results
```

### GraphQL API Testing
```bash
python src/main.py \
  --contract examples/schema.graphql \
  --base-url https://api.github.com/graphql \
  --auth github_auth.json \
  --contract-type graphql
```

### Smart Contract Testing
```bash
python src/main.py \
  --contract examples/erc20.abi.json \
  --base-url https://mainnet.infura.io/v3/YOUR_PROJECT_ID \
  --contract-type abi
```

### Performance Testing
```bash
python src/main.py \
  --contract examples/ecommerce_api.yaml \
  --metadata examples/ecommerce_metadata.yaml \
  --parallel 8 \
  --filter performance
```

### Security Testing
```bash
python src/main.py \
  --contract examples/swagger.yaml \
  --filter security \
  --verbose \
  --output-dir security_results
```

## 📁 Project Structure

```
api-testing-framework/
├── src/
│   ├── main.py                 # Main CLI application
│   ├── input_parser.py         # Contract format parsers
│   ├── test_generator.py       # Test case generation engine
│   ├── test_executor.py        # Test execution engine
│   ├── result_publisher.py     # Report generation
│   └── gherkin_generator.py    # Gherkin feature files
├── examples/
│   ├── swagger.yaml           # OpenAPI specification
│   ├── erc20.abi.json         # Smart contract ABI
│   ├── schema.graphql         # GraphQL schema
│   ├── sample_collection.json # Postman collection
│   ├── ecommerce_api.yaml     # Complex API spec
│   ├── ecommerce_metadata.yaml # Test metadata
│   ├── httpbin_test.yaml      # HTTPBin test spec
│   ├── config.yaml            # Basic configuration
│   └── blockchain_*.yaml      # Blockchain examples
├── output/                    # Generated test results
│   ├── api_tests.feature      # Gherkin features
│   ├── results.html          # HTML report
│   ├── results.json          # JSON results
│   └── api_test.log          # Execution logs
├── auth_config.json          # Authentication config
├── environments.json         # Environment configs
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/api-testing-framework.git
cd api-testing-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/ -v

# Run linting
flake8 src/ tests/
black src/ tests/
```

### Adding New Features
1. **Contract Parsers**: Extend `InputParser` for new formats
2. **Test Generators**: Add new test types in `TestGenerator`
3. **Auth Methods**: Implement new auth types in `TestExecutor`
4. **Validators**: Add custom assertions and validations
5. **Reporters**: Create new output formats in `ResultPublisher`

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Write unit tests for new features
- Update documentation for API changes
- Maintain backward compatibility

### Testing
```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests
python -m pytest tests/integration/ -v

# Generate coverage report
python -m pytest --cov=src --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by popular API testing tools like Postman, Insomnia, and REST Assured
- Built with modern Python libraries for reliability and performance
- Designed for enterprise API testing workflows

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/api-testing-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/api-testing-framework/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/api-testing-framework/wiki)

---

**Happy API Testing!** 🎉
