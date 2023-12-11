import unittest
from server.server import app
from unittest.mock import patch, Mock, MagicMock

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # Valid: authorized and correct format
    @patch('os.getenv', return_value="some_api_secret")
    @patch('relation_extraction.relation_extractor.RelationExtractor.begin_extraction', return_value=Mock())
    def test_do_tripleconstruction_valid_post_request(self, mock_begin_extraction, mock_os):
        response = self.app.post('/tripleconstruction', data=bytes('{"key": "value"}', 'utf-8'), headers={"Authorization": "some_api_secret"})
        json_response = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json_response)
        
        mock_os.assert_called_once_with("API_SECRET")
        mock_begin_extraction.assert_called_once_with({"key":"value"})
    
    # Invalid: authorized and incorrect format
    @patch('os.getenv', return_value="some_api_secret")
    @patch('relation_extraction.relation_extractor.RelationExtractor.begin_extraction', return_value=Mock())
    def test_do_tripleconstruction_incorrect_format(self, mock_begin_extraction, mock_os):
        response = self.app.post('/tripleconstruction', data=bytes('{"key": "value"', 'utf-8'), headers={"Authorization": "some_api_secret"})
        json_response = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertIn('error', json_response)
        
        mock_os.assert_called_once_with("API_SECRET")
        mock_begin_extraction.assert_not_called()

    # Invalid: unauthorized and correct format
    @patch('os.getenv', return_value="some_api_secret")
    @patch('relation_extraction.relation_extractor.RelationExtractor.begin_extraction', return_value=Mock())
    def test_do_tripleconstruction_unauthorized(self, mock_begin_extraction, mock_os):
        response = self.app.post('/tripleconstruction', data=bytes('{"key": "value"}','utf-8'), headers={"Authorization": "a_new_api_secret"})
        json_response = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)
        
        mock_os.assert_called_once_with("API_SECRET")
        mock_begin_extraction.assert_not_called()

    # Invalid endpoint
    @patch('os.getenv', return_value="some_api_secret")
    @patch('relation_extraction.relation_extractor.RelationExtractor.begin_extraction', return_value=Mock())
    def test_invalid_endpoint(self, mock_begin_extraction, mock_os):
        response = self.app.post('/triple-construction', data=bytes('{"key": "value"}', 'utf-8'), headers={"Authorization": "some_api_secret"})
        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', json_response)
        
        mock_os.assert_not_called()
        mock_begin_extraction.assert_not_called()
