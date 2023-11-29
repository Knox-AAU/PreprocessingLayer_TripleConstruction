import unittest
from relation_extraction.output import *
from unittest.mock import patch, Mock, MagicMock

class TestOutput(unittest.TestCase):
    
    def test_format_output(self):
        input = [["this", "is", "triples"]]
        res = format_output(input)
        self.assertTrue("triples" in res.keys())
        self.assertEqual(res["triples"], input)

    @patch("requests.post")
    def test_send_to_database(self, mock_request):
        mock_response = MagicMock()
        mock_response.text = "response"
        mock_request.return_value = mock_response
        res = send_to_database_component("test_output")

        mock_request.assert_called_once_with(url='http://130.225.57.13/knox-api/triples', json={'triples': 'test_output'}, params={'g': 'http://knox_database'}, headers={'Access-Authorization': 'internal_key'})
        self.assertEqual(res, "response")