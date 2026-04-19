import random
import string
from typing import Dict, Any, List

class TestGenerator:
    """Generates positive, negative, and edge test cases from API definitions."""

    def __init__(self, endpoints: List[Dict[str, Any]], schemas: Dict[str, Any], metadata: Dict[str, Any] = None):
        self.endpoints = endpoints
        self.schemas = schemas
        self.metadata = metadata or {}

    def generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generates a comprehensive set of test cases for all endpoints."""
        test_cases = []
        for endpoint in self.endpoints:
            test_cases.extend(self._generate_positive_tests(endpoint))
            test_cases.extend(self._generate_negative_tests(endpoint))
            test_cases.extend(self._generate_edge_cases(endpoint))
        return test_cases

    def _generate_positive_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates positive test cases with valid inputs."""
        test_cases = []
        # Basic positive test case
        test_cases.append({
            'name': f"Positive: {endpoint['method']} {endpoint['path']}",
            'endpoint': endpoint,
            'type': 'positive',
            'parameters': self._generate_valid_parameters(endpoint),
            'request_body': self._generate_valid_request_body(endpoint),
            'expected_status': 200 # Default positive status code
        })
        return test_cases

    def _generate_negative_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates negative test cases with invalid inputs."""
        test_cases = []
        # Negative test case: Missing required parameters
        required_params = [p for p in endpoint.get('parameters', []) if p.get('required')]
        for param in required_params:
            test_cases.append({
                'name': f"Negative: Missing required parameter '{param['name']}' in {endpoint['method']} {endpoint['path']}",
                'endpoint': endpoint,
                'type': 'negative',
                'parameters': self._generate_valid_parameters(endpoint, exclude=[param['name']]),
                'request_body': self._generate_valid_request_body(endpoint),
                'expected_status': 400 # Default negative status code
            })
        # Negative test case: Invalid data types
        for param in endpoint.get('parameters', []):
            test_cases.append({
                'name': f"Negative: Invalid data type for parameter '{param['name']}' in {endpoint['method']} {endpoint['path']}",
                'endpoint': endpoint,
                'type': 'negative',
                'parameters': self._generate_invalid_parameters(endpoint, param['name']),
                'request_body': self._generate_valid_request_body(endpoint),
                'expected_status': 400
            })
        return test_cases

    def _generate_edge_cases(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates edge test cases with boundary values."""
        test_cases = []
        # Edge case: Empty/null values for optional parameters
        optional_params = [p for p in endpoint.get('parameters', []) if not p.get('required')]
        for param in optional_params:
            test_cases.append({
                'name': f"Edge: Null value for optional parameter '{param['name']}' in {endpoint['method']} {endpoint['path']}",
                'endpoint': endpoint,
                'type': 'edge',
                'parameters': self._generate_valid_parameters(endpoint, null_params=[param['name']]),
                'request_body': self._generate_valid_request_body(endpoint),
                'expected_status': 200 # Should still be successful
            })
        return test_cases

    def _generate_valid_parameters(self, endpoint: Dict[str, Any], exclude: List[str] = None, null_params: List[str] = None) -> Dict[str, Any]:
        """Generates valid parameter values based on schema definitions."""
        params = {}
        exclude = exclude or []
        null_params = null_params or []
        for param in endpoint.get('parameters', []):
            if param['name'] in exclude:
                continue
            if param['name'] in null_params:
                params[param['name']] = None
                continue
            # Generate valid value based on type
            param_type = param.get('schema', {}).get('type', 'string')
            params[param['name']] = self._generate_value_by_type(param_type)
        return params

    def _generate_invalid_parameters(self, endpoint: Dict[str, Any], target_param: str) -> Dict[str, Any]:
        """Generates parameter values with an invalid value for the target parameter."""
        params = self._generate_valid_parameters(endpoint)
        # Find the target parameter and set an invalid value
        for param in endpoint.get('parameters', []):
            if param['name'] == target_param:
                param_type = param.get('schema', {}).get('type', 'string')
                params[target_param] = self._generate_invalid_value_by_type(param_type)
                break
        return params

    def _generate_valid_request_body(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a valid request body based on schema definitions."""
        request_body = endpoint.get('requestBody', {})
        if not request_body:
            return {}
        content = request_body.get('content', {})
        if 'application/json' in content:
            schema_ref = content['application/json'].get('schema', {}).get('$ref')
            if schema_ref:
                schema_name = schema_ref.split('/')[-1]
                schema = self.schemas.get(schema_name, {})
                return self._generate_data_from_schema(schema)
        return {}

    def _generate_value_by_type(self, data_type: str) -> Any:
        """Generates a valid value for a given data type."""
        if data_type == 'string':
            return ''.join(random.choices(string.ascii_letters, k=10))
        elif data_type == 'integer':
            return random.randint(1, 100)
        elif data_type == 'boolean':
            return random.choice([True, False])
        elif data_type == 'number':
            return random.uniform(1.0, 100.0)
        return None

    def _generate_invalid_value_by_type(self, data_type: str) -> Any:
        """Generates an invalid value for a given data type."""
        if data_type == 'string':
            return 123 # Invalid type (integer instead of string)
        elif data_type == 'integer':
            return "not-an-integer" # Invalid type (string instead of integer)
        elif data_type == 'boolean':
            return "not-a-boolean"
        elif data_type == 'number':
            return "not-a-number"
        return None

    def _generate_data_from_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generates data based on a schema definition."""
        data = {}
        properties = schema.get('properties', {})
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get('type', 'string')
            data[prop_name] = self._generate_value_by_type(prop_type)
        return data
