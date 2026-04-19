import requests
from typing import Dict, Any, List

class TestExecutor:
    """Executes generated test cases against API endpoints."""

    def __init__(self, base_url: str, test_cases: List[Dict[str, Any]]):
        self.base_url = base_url
        self.test_cases = test_cases
        self.results = []

    def execute_tests(self) -> List[Dict[str, Any]]:
        """Executes all test cases and records the results."""
        for test_case in self.test_cases:
            result = self._execute_test_case(test_case)
            self.results.append(result)
        return self.results

    def _execute_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a single test case and returns the result."""
        endpoint = test_case['endpoint']
        path = endpoint['path']
        method = endpoint['method']
        params = test_case['parameters']
        request_body = test_case['request_body']
        expected_status = test_case['expected_status']

        url = f"{self.base_url}{path}"
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=request_body,
                timeout=10
            )
            actual_status = response.status_code
            passed = actual_status == expected_status
            return {
                'name': test_case['name'],
                'type': test_case['type'],
                'url': url,
                'method': method,
                'parameters': params,
                'request_body': request_body,
                'expected_status': expected_status,
                'actual_status': actual_status,
                'response_body': response.text,
                'passed': passed
            }
        except requests.exceptions.RequestException as e:
            return {
                'name': test_case['name'],
                'type': test_case['type'],
                'url': url,
                'method': method,
                'parameters': params,
                'request_body': request_body,
                'expected_status': expected_status,
                'actual_status': None,
                'response_body': str(e),
                'passed': False,
                'error': str(e)
            }
