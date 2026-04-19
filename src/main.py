import argparse
import os
from input_parser import InputParser
from test_generator import TestGenerator
from test_executor import TestExecutor
from result_publisher import ResultPublisher
from gherkin_generator import GherkinGenerator

def main():
    parser = argparse.ArgumentParser(description="No-code API Testing Tool")
    parser.add_argument("--spec", required=True, help="Path to Swagger/OpenAPI specification (JSON/YAML)")
    parser.add_argument("--metadata", help="Path to metadata/configuration file (YAML)")
    parser.add_argument("--base-url", required=True, help="Base URL of the API")
    parser.add_argument("--output-dir", default="output", help="Directory to save test results and Gherkin files")
    args = parser.parse_args()

    # 1. Parse Input
    print(f"Parsing specification: {args.spec}")
    input_parser = InputParser(args.spec, args.metadata)
    endpoints = input_parser.get_endpoints()
    schemas = input_parser.get_schemas()

    # 2. Generate Test Cases
    print("Generating test cases...")
    test_generator = TestGenerator(endpoints, schemas, input_parser.metadata)
    test_cases = test_generator.generate_test_cases()
    print(f"Generated {len(test_cases)} test cases.")

    # 3. Generate Gherkin Feature Files
    print("Generating Gherkin feature files...")
    gherkin_generator = GherkinGenerator(test_cases)
    feature_content = gherkin_generator.generate_feature_files()
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, 'api_tests.feature'), 'w') as f:
        f.write(feature_content)

    # 4. Execute Tests
    print(f"Executing tests against: {args.base_url}")
    test_executor = TestExecutor(args.base_url, test_cases)
    results = test_executor.execute_tests()

    # 5. Publish Results
    print(f"Publishing results to: {args.output_dir}")
    result_publisher = ResultPublisher(results, args.output_dir)
    result_publisher.publish_results()

    print("Test execution completed.")

if __name__ == "__main__":
    main()
