import requests
import time
from typing import Dict, Any, List

class TestExecutor:
    """Executes generated test cases against API endpoints."""

    def __init__(self, base_url: str, test_cases: List[Dict[str, Any]]):
        self.base_url = base_url
        self.test_cases = test_cases
        self.results = []

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
            if test_type == 'performance':
                # Handle performance testing
                return self._execute_performance_test(test_case)
            elif contract_type == 'smart_contract':
                # For smart contracts, might need different handling
                # For now, assume it's still HTTP-based
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=request_body,
                    timeout=10
                )
            elif contract_type == 'graphql':
                # GraphQL typically uses POST with query in body
                graphql_body = {
                    'query': request_body.get('query', ''),
                    'variables': request_body.get('variables', {})
                }
                response = requests.post(
                    url=url,
                    json=graphql_body,
                    timeout=10
                )
            else:
                # Default REST API execution
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=request_body,
                    timeout=10
                )
            
            actual_status = response.status_code
            passed = actual_status == expected_status
            
            # Additional assertions from metadata
            assertion_results = self._check_custom_assertions(test_case, response)
            
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
                'response_time': response.elapsed.total_seconds() * 1000  # in milliseconds
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
        
        # Basic response validation
        if response.status_code == 200:
            assertion_results['status_code_200'] = True
        else:
            assertion_results['status_code_200'] = False
        
        # Check response time if specified
        response_time = response.elapsed.total_seconds() * 1000
        if response_time < 5000:  # Basic timeout check
            assertion_results['response_time_ok'] = True
        else:
            assertion_results['response_time_ok'] = False
        
        # Check if response has content for successful requests
        if response.status_code in [200, 201] and not response.text.strip():
            assertion_results['has_response_content'] = False
        else:
            assertion_results['has_response_content'] = True
        
        # Check for common error patterns
        if 'error' in response.text.lower() or 'exception' in response.text.lower():
            assertion_results['no_error_in_response'] = False
        else:
            assertion_results['no_error_in_response'] = True
        
        return assertion_results
