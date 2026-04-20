import unittest
from openapi_spec_validator import validate_spec

class TestOpenAPIValidation(unittest.TestCase):

    def setUp(self):
        # Load your OpenAPI specification (YAML or JSON)
        # You might want to replace the path with the one corresponding to your setup
        self.spec_path = 'path/to/your/openapi_spec.yaml'

    def test_valid_openapi_spec(self):
        try:
            with open(self.spec_path) as spec_file:
                spec = spec_file.read()
            validate_spec(spec)
        except Exception as e:
            self.fail(f'OpenAPI validation failed: {e}')

if __name__ == '__main__':
    unittest.main()