import argparse
import os
import logging
import json
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from input_parser import InputParser
from test_generator import TestGenerator
from test_executor import TestExecutor
from result_publisher import ResultPublisher
from gherkin_generator import GherkinGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_test.log'),
        logging.StreamHandler()
    ]
)

def main():
    parser = argparse.ArgumentParser(description="Professional API Testing Tool")
    parser.add_argument("--contract", required=True, help="Path to contract/specification file")
    parser.add_argument("--metadata", nargs='+', help="Path(s) to metadata/configuration file(s) (YAML)")
    parser.add_argument("--base-url", help="Base URL of the API")
    parser.add_argument("--env", default="default", help="Environment configuration (dev, staging, prod)")
    parser.add_argument("--output-dir", default="output", help="Directory to save test results")
    parser.add_argument("--contract-type", help="Type of contract (openapi, abi, graphql, postman, auto)")
    parser.add_argument("--auth", help="Authentication config file")
    parser.add_argument("--parallel", type=int, default=1, help="Number of parallel test executions")
    parser.add_argument("--retry", type=int, default=0, help="Number of retries for failed tests")
    parser.add_argument("--filter", help="Filter tests by type (positive,negative,edge,security,data_driven,performance)")
    parser.add_argument("--tags", help="Filter tests by tags (comma-separated)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--validate-schema", action="store_true", help="Validate response schemas")
    parser.add_argument("--generate-report", action="store_true", default=True, help="Generate HTML/JSON reports")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load environment configuration
    env_config = load_environment_config(args.env, args.base_url)
    base_url = env_config.get('base_url')

    # Load authentication configuration
    auth_config = load_auth_config(args.auth) if args.auth else {}

    # Load metadata from one or more YAML files
    metadata = load_metadata_files(args.metadata)

    logging.info(f"Starting API testing with contract: {args.contract}")
    logging.info(f"Environment: {args.env}, Base URL: {base_url}")

    # 1. Parse Input
    input_parser = InputParser(args.contract, metadata_source=metadata, contract_type=args.contract_type)
    endpoints = input_parser.get_endpoints()
    schemas = input_parser.get_schemas()

    # 2. Generate Test Cases
    logging.info("Generating test cases...")
    test_generator = TestGenerator(endpoints, schemas, input_parser.metadata)
    test_cases = test_generator.generate_test_cases()

    # Apply filters
    if args.filter:
        filter_types = args.filter.split(',')
        test_cases = [tc for tc in test_cases if tc['type'] in filter_types]

    if args.tags:
        filter_tags = args.tags.split(',')
        test_cases = [tc for tc in test_cases if any(tag in tc.get('tags', []) for tag in filter_tags)]

    logging.info(f"Generated {len(test_cases)} test cases after filtering")

    # 3. Generate Gherkin Feature Files
    if test_cases:
        logging.info("Generating Gherkin feature files...")
        gherkin_generator = GherkinGenerator(test_cases)
        feature_content = gherkin_generator.generate_feature_files()
        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, 'api_tests.feature'), 'w') as f:
            f.write(feature_content)

    # 4. Execute Tests
    if test_cases:
        logging.info(f"Executing {len(test_cases)} tests against: {base_url}")

        if args.parallel > 1:
            results = execute_tests_parallel(test_cases, base_url, auth_config, args.parallel, args.retry, args.validate_schema)
        else:
            test_executor = TestExecutor(base_url, test_cases, auth_config, args.retry, args.validate_schema)
            results = test_executor.execute_tests()

        # 5. Publish Results
        if args.generate_report:
            logging.info(f"Publishing results to: {args.output_dir}")
            result_publisher = ResultPublisher(results, args.output_dir)
            result_publisher.publish_results()

    logging.info("Test execution completed")

def load_environment_config(env_name, base_url_override=None):
    """Load environment-specific configuration."""
    config = {
        'default': {'base_url': base_url_override or 'http://localhost:8000'},
        'dev': {'base_url': 'http://localhost:8000'},
        'staging': {'base_url': 'https://api-staging.example.com'},
        'prod': {'base_url': 'https://api.example.com'}
    }

    # Try to load from environments.json if it exists
    env_file = 'environments.json'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                config.update(json.load(f))
        except Exception as e:
            logging.warning(f"Could not load environment config: {e}")

    return config.get(env_name, config['default'])

def merge_metadata(base, override):
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            merge_metadata(base[key], value)
        else:
            base[key] = value
    return base

def load_metadata_files(metadata_paths):
    if not metadata_paths:
        return {}

    metadata = {}
    for path in metadata_paths:
        if not os.path.exists(path):
            logging.warning(f"Metadata file not found: {path}")
            continue
        try:
            with open(path, 'r') as f:
                loaded = yaml.safe_load(f) or {}
                merge_metadata(metadata, loaded)
        except Exception as e:
            logging.warning(f"Could not load metadata file {path}: {e}")
    return metadata


def load_auth_config(auth_file):
    """Load authentication configuration."""
    if not auth_file or not os.path.exists(auth_file):
        return {}

    try:
        with open(auth_file, 'r') as f:
            if auth_file.endswith('.json'):
                return json.load(f)
            else:
                return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Could not load auth config: {e}")
        return {}

def execute_tests_parallel(test_cases, base_url, auth_config, max_workers, retry_count, validate_schema):
    """Execute tests in parallel using thread pools."""
    results = []

    def execute_single_test(test_case):
        executor = TestExecutor(base_url, [test_case], auth_config, retry_count, validate_schema)
        return executor.execute_tests()[0]

    logging.info(f"Executing tests with {max_workers} parallel workers")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_test = {executor.submit(execute_single_test, tc): tc for tc in test_cases}

        for i, future in enumerate(as_completed(future_to_test), 1):
            test_case = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
                status = "PASS" if result['passed'] else "FAIL"
                logging.info(f"[{i}/{len(test_cases)}] {test_case['name']}: {status}")
            except Exception as exc:
                logging.error(f"Test {test_case['name']} generated an exception: {exc}")
                results.append({
                    'name': test_case['name'],
                    'passed': False,
                    'error': str(exc)
                })

    return results

if __name__ == "__main__":
    main()
