# No-Code API Testing Tool

This tool automates API testing by dynamically generating and executing test cases (positive, negative, and edge) based on Swagger/OpenAPI specifications and metadata configuration files. It also generates human-readable test scenarios in Gherkin syntax and publishes comprehensive test results in HTML and JSON formats.

## Features

- **No-Code Automation**: Define your API and test parameters using Swagger/OpenAPI and YAML files.
- **Dynamic Test Generation**: Automatically creates positive, negative, and edge test cases based on API schemas.
- **Gherkin Syntax Support**: Generates human-readable `.feature` files for collaboration and documentation.
- **Comprehensive Reporting**: Publishes detailed test results in HTML and JSON formats.
- **CLI Interface**: Easy-to-use command-line interface for running tests.

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
python src/main.py --spec examples/swagger.yaml --base-url http://api.example.com --output-dir output
```

### Arguments

- `--spec`: Path to the Swagger/OpenAPI specification (JSON/YAML).
- `--metadata`: (Optional) Path to the metadata/configuration file (YAML).
- `--base-url`: Base URL of the API to be tested.
- `--output-dir`: (Optional) Directory to save test results and Gherkin files (default: `output`).

## Project Structure

- `src/`: Source code for the tool.
- `examples/`: Sample Swagger/OpenAPI and configuration files.
- `tests/`: Unit tests for the tool.
- `output/`: Generated test results and Gherkin files.

## License

This project is licensed under the MIT License.
