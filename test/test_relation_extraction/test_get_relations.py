import unittest
from relation_extraction.ontology_messenger import OntologyMessenger
from server.server import *
from unittest.mock import patch, Mock, MagicMock, mock_open

class TestGetRelations(unittest.TestCase):

    @patch('os.getenv')
    @patch('requests.get')
    def test_extract_specific_relations(self, mock_get, mock_os):
        response = {
            "triples": [
                {"s": {"Value": "http://dbpedia.org/ontology/test"}},
                {"s": {"Value": "http://dbpedia.org/ontology/another_test"}}
            ]
        }
        
        mock_os.return_value = "internal_key"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response
        mock_get.return_value.text.return_value = "request response"
        
        relations = OntologyMessenger.send_request()
        
        self.assertEqual(len(relations), 2)
        self.assertEqual(relations[0], "test")
        self.assertEqual(relations[1], "another_test")
        mock_get.assert_called_once_with(url='http://knox-proxy01.srv.aau.dk/knox-api/triples', params={'g': 'http://knox_ontology', 's': 'http://dbpedia.org/ontology/', 'o': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'}, headers={'Access-Authorization': 'internal_key'})



if __name__ == "__main__":
    unittest.main()