import unittest
from server.server import *
from unittest.mock import patch, Mock, MagicMock, mock_open
from relation_extraction.get_relations import *

class TestGetRelations(unittest.TestCase):

    @patch('requests.get')
    def test_extract_specific_relations(self, mock_get):
        response = {
            "triples": [
                {"s": {"Value": "http://dbpedia.org/ontology/test"}},
                {"s": {"Value": "http://dbpedia.org/ontology/another_test"}}
            ]
        }
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response
        mock_get.return_value.text.return_value = "request response"
        
        relations = extract_specific_relations()
        
        self.assertEqual(len(relations), 2)
        self.assertEqual(relations[0], "test")
        self.assertEqual(relations[1], "another_test")
        mock_get.assert_called_once_with(url='http://130.225.57.13/knox-api/triples', params={'g': 'http://knox_ontology', 's': 'http://dbpedia.org/ontology/', 'o': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'}, headers={'Access-Authorization': 'internal_key'})


    @patch("builtins.open", new_callable=mock_open, read_data=":testline\na rdf:Property, owl:ObjectProperty ;")
    def test_extract_specific_relations_offline(self, mock_open):
        res = extract_specific_relations_offline()
        mock_open.assert_called_once()

        self.assertEqual(res, ["testline"])
  


if __name__ == "__main__":
    unittest.main()