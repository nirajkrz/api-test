import pytest
from unittest.mock import patch

@pytest.fixture
def mock_api_response():
    # Mock response data here
    return {
        'data': 'mocked data',
        'status': 'success'
    }

@pytest.fixture
def test_data():
    # Test data for API tests
    return [
        {'input': 'test1', 'expected': 'result1'},
        {'input': 'test2', 'expected': 'result2'}
    ]

@pytest.fixture
def api_client():
    # Set up your API client here
    return SomeApiClient()

# You can add more fixtures as needed
