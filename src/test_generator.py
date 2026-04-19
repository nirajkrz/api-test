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
            contract_type = endpoint.get('contract_type', 'rest_api')
            
            if contract_type == 'smart_contract':
                test_cases.extend(self._generate_smart_contract_tests(endpoint))
            elif contract_type == 'graphql':
                test_cases.extend(self._generate_graphql_tests(endpoint))
            else:
                # Default REST API tests
                test_cases.extend(self._generate_positive_tests(endpoint))
                test_cases.extend(self._generate_negative_tests(endpoint))
                test_cases.extend(self._generate_edge_cases(endpoint))
                test_cases.extend(self._generate_data_driven_tests(endpoint))
                test_cases.extend(self._generate_security_tests(endpoint))
        
        # Add performance tests if configured
        test_cases.extend(self._generate_performance_tests())
        
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
        """Generates a valid request body based on schema definitions and test data."""
        request_body = endpoint.get('requestBody', {})
        if not request_body:
            return {}
        
        content = request_body.get('content', {})
        if 'application/json' in content:
            schema_ref = content['application/json'].get('schema', {}).get('$ref')
            if schema_ref:
                schema_name = schema_ref.split('/')[-1]
                schema = self.schemas.get(schema_name, {})
                return self._generate_data_from_schema(schema, endpoint)
        
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

    def _generate_smart_contract_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates test cases for smart contract function calls."""
        test_cases = []
        # Basic function call test
        test_cases.append({
            'name': f"Smart Contract: Call {endpoint['path'][1:]} function",
            'endpoint': endpoint,
            'type': 'positive',
            'parameters': {},
            'request_body': self._generate_valid_request_body(endpoint),
            'expected_status': 200,  # Assuming successful execution
            'contract_type': 'smart_contract'
        })
        return test_cases

    def _generate_graphql_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates test cases for GraphQL queries/mutations."""
        test_cases = []
        # Basic GraphQL test
        test_cases.append({
            'name': f"GraphQL: Execute query on {endpoint['path']}",
            'endpoint': endpoint,
            'type': 'positive',
            'parameters': {},
            'request_body': {'query': 'query { test }', 'variables': {}},
            'expected_status': 200,
            'contract_type': 'graphql'
        })
        return test_cases

    def _generate_data_driven_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates data-driven test cases from metadata."""
        test_cases = []
        data_driven_scenarios = self.metadata.get('data_driven_scenarios', [])
        
        for scenario in data_driven_scenarios:
            if scenario.get('endpoint') == endpoint['path'] and scenario.get('method') == endpoint['method']:
                for test_case_data in scenario.get('test_cases', []):
                    test_cases.append({
                        'name': f"Data-driven: {scenario['name']} - {test_case_data}",
                        'endpoint': endpoint,
                        'type': 'data_driven',
                        'parameters': test_case_data.get('params', {}),
                        'request_body': test_case_data.get('body', {}),
                        'expected_status': test_case_data.get('expected_status', 200)
                    })
        
        return test_cases

    def _generate_security_tests(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates security test cases."""
        test_cases = []
        security_tests = self.metadata.get('security_tests', [])
        
        for sec_test in security_tests:
            if sec_test.get('endpoint') == endpoint['path'] and sec_test.get('method') == endpoint['method']:
                test_cases.append({
                    'name': f"Security: {sec_test['name']}",
                    'endpoint': endpoint,
                    'type': 'security',
                    'parameters': sec_test.get('params', {}),
                    'request_body': sec_test.get('body', {}),
                    'expected_status': sec_test.get('expected_status', 400)
                })
        
        # Add common security tests
        path = endpoint['path']
        method = endpoint['method']
        
        # SQL Injection tests for query parameters
        for param in endpoint.get('parameters', []):
            if param.get('in') == 'query' and param.get('schema', {}).get('type') == 'string':
                test_cases.append({
                    'name': f"Security: SQL Injection in {param['name']} - {method} {path}",
                    'endpoint': endpoint,
                    'type': 'security',
                    'parameters': {param['name']: "'; DROP TABLE users; --"},
                    'request_body': {},
                    'expected_status': 400
                })
        
        # XSS tests for string inputs
        if endpoint.get('requestBody'):
            test_cases.append({
                'name': f"Security: XSS in request body - {method} {path}",
                'endpoint': endpoint,
                'type': 'security',
                'parameters': {},
                'request_body': {'name': "<script>alert('xss')</script>"},
                'expected_status': 400
            })
        
        return test_cases

    def _generate_performance_tests(self) -> List[Dict[str, Any]]:
        """Generates performance test cases."""
        test_cases = []
        performance_tests = self.metadata.get('performance_tests', [])
        
        for perf_test in performance_tests:
            # Create a single test case that represents the performance test
            endpoint = None
            for ep in self.endpoints:
                if ep['path'] == perf_test.get('endpoint') and ep['method'] == perf_test.get('method'):
                    endpoint = ep
                    break
            
            if endpoint:
                test_cases.append({
                    'name': f"Performance: {perf_test['name']}",
                    'endpoint': endpoint,
                    'type': 'performance',
                    'parameters': {},
                    'request_body': {},
                    'expected_status': 200,
                    'performance_config': perf_test
                })
        
        return test_cases

    def _get_test_data_for_endpoint(self, endpoint_path: str = None) -> Dict[str, Any]:
        """Gets test data from metadata for a specific endpoint."""
        if not endpoint_path:
            return {}
        
        test_data = self.metadata.get('test_data', {})
        
        # Map endpoint paths to test data keys
        path_to_data_map = {
            '/users': 'users',
            '/products': 'products',
            '/orders': 'orders'
        }
        
        data_key = path_to_data_map.get(endpoint_path)
        if data_key and data_key in test_data:
            # Return first item or random item from test data
            data_items = test_data[data_key]
            if isinstance(data_items, list) and data_items:
                return random.choice(data_items)
            return data_items
        
        return {}

    def _generate_value_by_schema(self, prop_details: Dict[str, Any], is_required: bool = False) -> Any:
        """Generates a value based on detailed schema constraints."""
        prop_type = prop_details.get('type', 'string')
        
        if prop_type == 'string':
            return self._generate_string_value(prop_details, is_required)
        elif prop_type == 'integer':
            return self._generate_integer_value(prop_details)
        elif prop_type == 'number':
            return self._generate_number_value(prop_details)
        elif prop_type == 'boolean':
            return random.choice([True, False])
        elif prop_type == 'array':
            return self._generate_array_value(prop_details)
        elif prop_type == 'object':
            return self._generate_data_from_schema(prop_details)
        
        return None

    def _generate_string_value(self, prop_details: Dict[str, Any], is_required: bool = False) -> str:
        """Generates a string value with constraints."""
        min_length = prop_details.get('minLength', 0)
        max_length = prop_details.get('maxLength', 50)
        enum_values = prop_details.get('enum', [])
        
        if enum_values:
            return random.choice(enum_values)
        
        # Generate string of appropriate length
        length = random.randint(min_length, min(max_length, 20))
        if length == 0 and not is_required:
            return ""
        
        return ''.join(random.choices(string.ascii_letters + string.digits, k=max(1, length)))

    def _generate_integer_value(self, prop_details: Dict[str, Any]) -> int:
        """Generates an integer value with constraints."""
        minimum = prop_details.get('minimum', 0)
        maximum = prop_details.get('maximum', 1000)
        return random.randint(minimum, maximum)

    def _generate_number_value(self, prop_details: Dict[str, Any]) -> float:
        """Generates a number value with constraints."""
        minimum = prop_details.get('minimum', 0.0)
        maximum = prop_details.get('maximum', 1000.0)
        return round(random.uniform(minimum, maximum), 2)

    def _generate_array_value(self, prop_details: Dict[str, Any]) -> List[Any]:
        """Generates an array value."""
        items_schema = prop_details.get('items', {})
        min_items = prop_details.get('minItems', 0)
        max_items = prop_details.get('maxItems', 5)
        
        count = random.randint(min_items, max_items)
        return [self._generate_value_by_schema(items_schema) for _ in range(count)]

    def _generate_data_from_schema(self, schema: Dict[str, Any], endpoint: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generates data based on a schema definition with intelligent defaults."""
        data = {}
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        
        # Try to use test data from metadata first
        endpoint_path = endpoint['path'] if endpoint else None
        test_data = self._get_test_data_for_endpoint(endpoint_path)
        
        for prop_name, prop_details in properties.items():
            if prop_name in test_data:
                # Use test data if available
                data[prop_name] = test_data[prop_name]
            else:
                # Generate based on schema constraints
                data[prop_name] = self._generate_value_by_schema(prop_details, prop_name in required)
        
        return data
