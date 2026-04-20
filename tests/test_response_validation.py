import unittest

class TestResponseValidation(unittest.TestCase):

    def test_valid_response(self):
        # Simulate a valid response to validate
        response = {
            'status': 'success',
            'data': {'id': 1, 'name': 'Test'}
        }
        self.assertEqual(response['status'], 'success')
        self.assertIn('data', response)

    def test_invalid_response(self):
        # Simulate an invalid response to validate
        response = {
            'status': 'error',
            'message': 'Not Found'
        }
        self.assertEqual(response['status'], 'error')
        self.assertIn('message', response)

if __name__ == '__main__':
    unittest.main()