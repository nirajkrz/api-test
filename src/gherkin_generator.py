import json
from typing import Dict, Any, List

class GherkinGenerator:
    """Generates Gherkin feature files from test cases."""

    def __init__(self, test_cases: List[Dict[str, Any]]):
        self.test_cases = test_cases

    def generate_feature_files(self) -> str:
        """Generates a single Gherkin feature file containing all test scenarios."""
        feature_content = "Feature: API Testing Scenarios\n\n"
        for test_case in self.test_cases:
            feature_content += self._generate_scenario(test_case)
        return feature_content

    def _generate_scenario(self, test_case: Dict[str, Any]) -> str:
        """Generates a Gherkin scenario for a single test case."""
        scenario_name = test_case['name']
        endpoint = test_case['endpoint']
        path = endpoint['path']
        method = endpoint['method']
        params = test_case['parameters']
        request_body = test_case['request_body']
        expected_status = test_case['expected_status']

        scenario = f"  Scenario: {scenario_name}\n"
        scenario += f"    Given the API endpoint '{path}' is available\n"
        if params:
            scenario += f"    And the following query parameters are provided:\n"
            scenario += f"      | Parameter | Value |\n"
            for name, value in params.items():
                scenario += f"      | {name} | {value} |\n"
        if request_body:
            scenario += f"    And the following request body is provided:\n"
            scenario += f"      \"\"\"\n"
            scenario += f"      {json.dumps(request_body, indent=2)}\n"
            scenario += f"      \"\"\"\n"
        scenario += f"    When a {method} request is sent to the endpoint\n"
        scenario += f"    Then the response status code should be {expected_status}\n\n"
        return scenario
