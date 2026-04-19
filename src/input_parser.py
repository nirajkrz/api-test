import os
import yaml
import requests
import json
from typing import Dict, Any, List

class InputParser:
    """Parses various contract/specification formats and metadata files."""

    def __init__(self, contract_path: str, metadata_source=None, contract_type: str = None):
        self.contract_path = contract_path
        self.metadata_source = metadata_source
        self.contract_type = contract_type or self._detect_contract_type()
        self.contract = self._load_contract()
        self.metadata = self._load_metadata()

    def _detect_contract_type(self) -> str:
        """Automatically detects the contract type based on file content."""
        try:
            content = self._load_raw_contract()
            if isinstance(content, dict):
                if 'openapi' in content or 'swagger' in content:
                    return 'openapi'
                elif 'abi' in content or (isinstance(content, list) and content and 'type' in content[0]):
                    return 'abi'
                elif 'type' in content and content.get('type') == 'Query':
                    return 'graphql'
                elif 'info' in content and 'item' in content:
                    return 'postman'
            elif isinstance(content, str):
                if 'type Query' in content or 'type Mutation' in content:
                    return 'graphql'
        except:
            pass
        return 'openapi'  # Default fallback

    def _load_raw_contract(self) -> Any:
        """Loads the contract file without parsing."""
        if self.contract_path.startswith(('http://', 'https://')):
            response = requests.get(self.contract_path)
            response.raise_for_status()
            try:
                return response.json()
            except json.JSONDecodeError:
                return yaml.safe_load(response.text)
        else:
            with open(self.contract_path, 'r') as f:
                if self.contract_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(f)
                elif self.contract_path.endswith('.json'):
                    return json.load(f)
                elif self.contract_path.endswith('.graphql') or self.contract_path.endswith('.gql'):
                    # Return GraphQL schema as string
                    return f.read()
                else:
                    # Try JSON first, then YAML, then treat as GraphQL string
                    try:
                        return json.load(f)
                    except json.JSONDecodeError:
                        f.seek(0)
                        try:
                            return yaml.safe_load(f)
                        except yaml.YAMLError:
                            f.seek(0)
                            return f.read()  # Assume GraphQL or other text format

    def _load_contract(self) -> Dict[str, Any]:
        """Loads and parses the contract based on detected type."""
        raw_content = self._load_raw_contract()
        
        if self.contract_type == 'openapi':
            return self._parse_openapi(raw_content)
        elif self.contract_type == 'abi':
            return self._parse_abi(raw_content)
        elif self.contract_type == 'graphql':
            return self._parse_graphql(raw_content)
        elif self.contract_type == 'postman':
            return self._parse_postman(raw_content)
        else:
            # Default to OpenAPI parsing
            return self._parse_openapi(raw_content)

    def _parse_openapi(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Parses OpenAPI/Swagger specification."""
        return content

    def _parse_abi(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parses Ethereum smart contract ABI."""
        # Convert ABI to OpenAPI-like structure
        openapi_like = {
            'paths': {},
            'components': {'schemas': {}}
        }
        
        for item in content:
            if item.get('type') == 'function':
                method_name = item['name']
                inputs = item.get('inputs', [])
                outputs = item.get('outputs', [])
                
                # Create path for function call
                path = f"/{method_name}"
                openapi_like['paths'][path] = {
                    'post': {
                        'summary': f"Call {method_name} function",
                        'parameters': [],
                        'requestBody': {
                            'required': True,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {inp['name']: {'type': self._map_abi_type(inp['type'])} for inp in inputs},
                                        'required': [inp['name'] for inp in inputs if not inp.get('indexed', False)]
                                    }
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'Function executed successfully',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {out['name']: {'type': self._map_abi_type(out['type'])} for out in outputs}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
        
        return openapi_like

    def _parse_graphql(self, content: str) -> Dict[str, Any]:
        """Parses GraphQL schema (simplified)."""
        # This is a basic parser - in production, use a proper GraphQL parser
        openapi_like = {
            'paths': {},
            'components': {'schemas': {}}
        }
        
        # Basic parsing for demonstration
        if 'type Query' in content:
            # Extract queries
            openapi_like['paths']['/graphql'] = {
                'post': {
                    'summary': 'GraphQL Query',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'query': {'type': 'string'},
                                        'variables': {'type': 'object'}
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'Query executed successfully'}
                    }
                }
            }
        
        return openapi_like

    def _parse_postman(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Parses Postman collection."""
        openapi_like = {
            'paths': {},
            'components': {'schemas': {}}
        }
        
        def process_item(item):
            if 'request' in item:
                method = item['request'].get('method', 'GET').lower()
                url = item['request'].get('url', {})
                if isinstance(url, dict) and 'raw' in url:
                    path = url['raw'].replace('{{base_url}}', '')
                else:
                    path = str(url)
                
                if path not in openapi_like['paths']:
                    openapi_like['paths'][path] = {}
                
                openapi_like['paths'][path][method] = {
                    'summary': item.get('name', ''),
                    'responses': {'200': {'description': 'Success'}}
                }
            
            if 'item' in item:
                for sub_item in item['item']:
                    process_item(sub_item)
        
        if 'item' in content:
            for item in content['item']:
                process_item(item)
        
        return openapi_like

    def _map_abi_type(self, abi_type: str) -> str:
        """Maps ABI types to OpenAPI types."""
        type_mapping = {
            'uint256': 'integer',
            'int256': 'integer',
            'address': 'string',
            'bool': 'boolean',
            'string': 'string',
            'bytes': 'string',
            'bytes32': 'string'
        }
        return type_mapping.get(abi_type, 'string')

    def _load_metadata(self) -> Dict[str, Any]:
        """Loads metadata/configuration from YAML files, dicts, or other sources."""
        if not self.metadata_source:
            return {}

        if isinstance(self.metadata_source, dict):
            return self.metadata_source

        if isinstance(self.metadata_source, (list, tuple)):
            metadata = {}
            for source in self.metadata_source:
                if isinstance(source, dict):
                    metadata.update(source)
                elif isinstance(source, str) and os.path.exists(source):
                    with open(source, 'r') as f:
                        metadata.update(yaml.safe_load(f) or {})
            return metadata

        if isinstance(self.metadata_source, str):
            if os.path.exists(self.metadata_source):
                with open(self.metadata_source, 'r') as f:
                    return yaml.safe_load(f) or {}

        return {}

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Extracts endpoint information from the parsed contract."""
        endpoints = []
        paths = self.contract.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),
                    'responses': details.get('responses', {})
                }
                
                # Add contract-specific metadata
                if self.contract_type == 'abi':
                    endpoint['contract_type'] = 'smart_contract'
                elif self.contract_type == 'graphql':
                    endpoint['contract_type'] = 'graphql'
                elif self.contract_type == 'postman':
                    endpoint['contract_type'] = 'postman'
                else:
                    endpoint['contract_type'] = 'rest_api'
                
                endpoints.append(endpoint)
        return endpoints

    def get_schemas(self) -> Dict[str, Any]:
        """Extracts schema definitions from the parsed contract."""
        components = self.contract.get('components', {})
        return components.get('schemas', {})
