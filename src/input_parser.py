import yaml
import requests
import json
from typing import Dict, Any, List

class InputParser:
    """Parses Swagger/OpenAPI specifications and metadata files."""

    def __init__(self, spec_path: str, metadata_path: str = None):
        self.spec_path = spec_path
        self.metadata_path = metadata_path
        self.spec = self._load_spec()
        self.metadata = self._load_metadata()

    def _load_spec(self) -> Dict[str, Any]:
        """Loads the Swagger/OpenAPI specification from a file or URL."""
        if self.spec_path.startswith(('http://', 'https://')):
            response = requests.get(self.spec_path)
            response.raise_for_status()
            try:
                return response.json()
            except json.JSONDecodeError:
                return yaml.safe_load(response.text)
        else:
            with open(self.spec_path, 'r') as f:
                if self.spec_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(f)
                else:
                    return json.load(f)

    def _load_metadata(self) -> Dict[str, Any]:
        """Loads metadata/configuration from a YAML or properties file."""
        if not self.metadata_path:
            return {}
        with open(self.metadata_path, 'r') as f:
            if self.metadata_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            # Add support for .properties if needed
            return {}

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Extracts endpoint information from the specification."""
        endpoints = []
        paths = self.spec.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                endpoints.append({
                    'path': path,
                    'method': method.upper(),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),
                    'responses': details.get('responses', {})
                })
        return endpoints

    def get_schemas(self) -> Dict[str, Any]:
        """Extracts schema definitions from the specification."""
        components = self.spec.get('components', {})
        return components.get('schemas', {})
