# No-Code API Testing Tool

This tool automates API testing by dynamically generating and executing comprehensive test suites based on various contract specifications and metadata. It supports REST APIs (OpenAPI/Swagger), smart contract ABIs, GraphQL schemas, Postman collections, and other metadata formats. The tool generates human-readable test scenarios in Gherkin syntax and publishes detailed test results in HTML and JSON formats.

## Features

- **Multi-Format Support**: Accepts OpenAPI/Swagger, smart contract ABIs, GraphQL schemas, Postman collections, and custom metadata
- **Dynamic Test Generation**: Automatically creates positive, negative, and edge test cases based on contract specifications
- **Contract-Aware Testing**: Tailors test generation and execution based on contract type (REST, smart contracts, GraphQL, etc.)
- **Gherkin Syntax Support**: Generates human-readable `.feature` files for collaboration and documentation
- **Comprehensive Reporting**: Publishes detailed test results in HTML and JSON formats with contract type information
- **CLI Interface**: Easy-to-use command-line interface for running tests against any supported contract format

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/api-tester.git
    cd api-tester
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool using the following command:

```bash
python src/main.py --contract examples/swagger.yaml --base-url http://api.example.com --output-dir output
```

### Arguments

- `--contract`: Path to the contract/specification file (OpenAPI/Swagger, ABI JSON, GraphQL schema, Postman collection, etc.)
- `--metadata`: (Optional) Path to the metadata/configuration file (YAML)
- `--base-url`: Base URL of the API/contract endpoint to be tested
- `--output-dir`: (Optional) Directory to save test results and Gherkin files (default: `output`)
- `--contract-type`: (Optional) Force specific contract type (openapi, abi, graphql, postman, auto)

## Supported Contract Formats

### OpenAPI/Swagger
```bash
python src/main.py --contract examples/swagger.yaml --base-url http://api.example.com
```

### Smart Contract ABI
```bash
python src/main.py --contract contract.abi.json --base-url https://ethereum-node.com --contract-type abi
```

### GraphQL Schema
```bash
python src/main.py --contract schema.graphql --base-url https://graphql-api.com/graphql --contract-type graphql
```

### Postman Collection
```bash
python src/main.py --contract collection.json --base-url http://api.example.com --contract-type postman
```

## Project Structure

- `src/`: Source code for the tool
- `examples/`: Sample contract files and configuration files
- `tests/`: Unit tests for the tool
- `output/`: Generated test results and Gherkin files

## License

This project is licensed under the MIT License.
