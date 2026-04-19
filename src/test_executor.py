import requests
import time
import logging
import json
from typing import Dict, Any, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class TestExecutor:
    """Executes generated test cases against API endpoints with professional features."""

    def __init__(self, base_url: str, test_cases: List[Dict[str, Any]], auth_config: Dict[str, Any] = None,
                 retry_count: int = 0, validate_schema: bool = False):
        self.base_url = base_url
        self.test_cases = test_cases
        self.auth_config = auth_config or {}
        self.retry_count = retry_count
        self.validate_schema = validate_schema
        self.results = []  # Initialize results list
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a configured requests session with authentication and retry logic."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retry_count,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Configure authentication
        self._configure_authentication(session)

        return session

    def _configure_authentication(self, session: requests.Session):
        """Configure authentication for the session."""
        auth_type = self.auth_config.get('type', '').lower()

        if auth_type == 'basic':
            from requests.auth import HTTPBasicAuth
            session.auth = HTTPBasicAuth(
                self.auth_config.get('username'),
                self.auth_config.get('password')
            )
        elif auth_type == 'bearer':
            session.headers.update({
                'Authorization': f"Bearer {self.auth_config.get('token')}"
            })
        elif auth_type == 'api_key':
            header_name = self.auth_config.get('header_name', 'X-API-Key')
            session.headers.update({
                header_name: self.auth_config.get('api_key')
            })
        elif auth_type == 'oauth2':
            # For OAuth2, we would typically refresh tokens here
            session.headers.update({
                'Authorization': f"Bearer {self.auth_config.get('access_token')}"
            })

    def execute_tests(self) -> List[Dict[str, Any]]:
        """Executes all test cases and records the results."""
        print(f"\n{'='*60}")
        print("EXECUTING TEST CASES")
        print(f"{'='*60}")

        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}] Executing: {test_case['name']}")
            result = self._execute_test_case(test_case)

            status = "PASS" if result['passed'] else "FAIL"
            status_color = "✓" if result['passed'] else "✗"
            print(f"Result: {status_color} {status}")

            if not result['passed']:
                print(f"  Expected: {result['expected_status']}, Got: {result['actual_status']}")
                if 'error' in result:
                    print(f"  Error: {result['error']}")

            self.results.append(result)

        print(f"\n{'='*60}")
        passed_count = sum(1 for r in self.results if r['passed'])
        print(f"SUMMARY: {passed_count}/{len(self.results)} tests passed")
        print(f"{'='*60}\n")

        return self.results

    def _execute_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a single test case and returns the result."""
        endpoint = test_case['endpoint']
        path = endpoint['path']
        method = endpoint['method']
        params = test_case['parameters']
        request_body = test_case['request_body']
        expected_status = test_case['expected_status']
        contract_type = test_case.get('contract_type', 'rest_api')
        test_type = test_case.get('type', 'positive')

        url = f"{self.base_url}{path}"
        
        try:
            start_time = time.time()

            if test_type == 'performance':
                # Handle performance testing
                result = self._execute_performance_test(test_case)
                result['response_time'] = time.time() - start_time
                return result

            # Prepare request
            request_kwargs = self._prepare_request(endpoint, params, request_body, contract_type)

            # Make request using session
            response = self.session.request(method=method, url=url, **request_kwargs)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000

            actual_status = response.status_code
            passed = actual_status == expected_status

            # Additional validations
            assertion_results = self._check_custom_assertions(test_case, response)

            # Schema validation if enabled
            if self.validate_schema and endpoint.get('responses', {}).get(str(expected_status)):
                schema_validation = self._validate_response_schema(response, endpoint, expected_status)
                assertion_results.update(schema_validation)

            # Log request/response for debugging
            logging.debug(f"Request: {method} {url}")
            logging.debug(f"Response: {actual_status}, Time: {response_time:.2f}ms")

            return {
                'name': test_case['name'],
                'type': test_type,
                'url': url,
                'method': method,
                'parameters': params,
                'request_body': request_body,
                'expected_status': expected_status,
                'actual_status': actual_status,
                'response_body': response.text,
                'passed': passed and all(assertion_results.values()),
                'contract_type': contract_type,
                'assertions': assertion_results,
                'response_time': response_time,
                'request_headers': dict(response.request.headers),
                'response_headers': dict(response.headers)
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'name': test_case['name'],
                'type': test_type,
                'url': url,
                'method': method,
                'parameters': params,
                'request_body': request_body,
                'expected_status': expected_status,
                'actual_status': None,
                'response_body': str(e),
                'passed': False,
                'error': str(e),
                'contract_type': contract_type,
                'assertions': {},
                'response_time': None
            }

    def _execute_performance_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a performance test case."""
        perf_config = test_case.get('performance_config', {})
        endpoint = test_case['endpoint']
        
        # Simple performance test - make multiple requests
        concurrent_users = perf_config.get('concurrent_users', 5)
        duration_seconds = perf_config.get('duration_seconds', 10)
        
        # For simplicity, we'll just make a few requests sequentially
        # In a real implementation, you'd use threading or asyncio
        response_times = []
        success_count = 0
        
        for i in range(min(10, concurrent_users)):  # Limit to 10 requests for demo
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint['path']}", timeout=5)
                end_time = time.time()
                
                response_times.append((end_time - start_time) * 1000)
                if response.status_code == 200:
                    success_count += 1
            except:
                response_times.append(5000)  # 5 second timeout as failure
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0
        error_rate = ((len(response_times) - success_count) / len(response_times)) * 100 if response_times else 0
        
        # Check performance assertions
        assertions = perf_config.get('assertions', [])
        assertion_results = {}
        
        for assertion in assertions:
            if assertion['type'] == 'response_time_p95':
                assertion_results['p95_response_time'] = p95_response_time <= assertion.get('max_ms', 1000)
            elif assertion['type'] == 'error_rate':
                assertion_results['error_rate'] = error_rate <= assertion.get('max_percent', 5)
        
        passed = all(assertion_results.values())
        
        return {
            'name': test_case['name'],
            'type': 'performance',
            'url': f"{self.base_url}{endpoint['path']}",
            'method': endpoint['method'],
            'parameters': {},
            'request_body': {},
            'expected_status': 200,
            'actual_status': 200 if success_count > 0 else 500,
            'response_body': f"Performance test completed. Avg: {avg_response_time:.2f}ms, P95: {p95_response_time:.2f}ms, Errors: {error_rate:.1f}%",
            'passed': passed,
            'contract_type': 'rest_api',
            'assertions': assertion_results,
            'performance_metrics': {
                'avg_response_time': avg_response_time,
                'p95_response_time': p95_response_time,
                'error_rate': error_rate,
                'total_requests': len(response_times)
            }
        }

    def _check_custom_assertions(self, test_case: Dict[str, Any], response) -> Dict[str, bool]:
        """Checks custom assertions defined in metadata."""
        assertion_results = {}
        
        try:
            response_json = response.json()
        except:
            response_json = None
        
        expected_status = test_case.get('expected_status', 200)
        assertion_results['status_code_match'] = response.status_code == expected_status

        # Check for common error patterns
        if 'error' in response.text.lower() or 'exception' in response.text.lower():
            assertion_results['no_error_in_response'] = False
        else:
            assertion_results['no_error_in_response'] = True
        
        return assertion_results

    def _prepare_request(self, endpoint: Dict[str, Any], params: Dict[str, Any],
                        request_body: Any, contract_type: str) -> Dict[str, Any]:
        """Prepare request parameters for different contract types."""
        request_kwargs = {'params': params}

        if contract_type == 'graphql':
            # GraphQL typically uses POST with query in body
            graphql_body = {
                'query': request_body.get('query', ''),
                'variables': request_body.get('variables', {})
            }
            request_kwargs['json'] = graphql_body
        elif request_body:
            # Default JSON body for REST APIs
            request_kwargs['json'] = request_body

        return request_kwargs

    def _validate_response_schema(self, response: requests.Response, endpoint: Dict[str, Any], status_code: int) -> Dict[str, bool]:
        """Validate response against JSON schema."""
        try:
            import jsonschema
            from jsonschema import validate

            response_spec = endpoint.get('responses', {}).get(str(status_code), {})
            content_spec = response_spec.get('content', {}).get('application/json', {})
            schema = content_spec.get('schema', {})

            if schema:
                response_json = response.json()
                validate(instance=response_json, schema=schema)
                return {'schema_validation': True}
            else:
                return {'schema_validation': True}  # No schema to validate against

        except ImportError:
            logging.warning("jsonschema not installed, skipping schema validation")
            return {'schema_validation': True}
        except jsonschema.ValidationError as e:
            logging.error(f"Schema validation failed: {e}")
            return {'schema_validation': False}
        except json.JSONDecodeError:
            # Response is not JSON, skip schema validation
            return {'schema_validation': True}
        except Exception as e:
            logging.error(f"Schema validation error: {e}")
            return {'schema_validation': False}
