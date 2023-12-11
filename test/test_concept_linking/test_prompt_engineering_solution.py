import json
import unittest
from unittest.mock import patch, MagicMock

from concept_linking.solutions.PromptEngineering import main
from concept_linking.solutions.PromptEngineering.main import api_url, headers


class TestPromptEngineering(unittest.TestCase):

    @patch('concept_linking.solutions.PromptEngineering.main.requests.post')
    def test_classify_entity_mentions_known(self, mock_post):
        expected_result = [
            (
                "knox-kb01.srv.aau.dk/Barack_Obama",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/Agent"
            )
        ]

        input_data = [
            {
                "fileName": "Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barack Obama is an agent.",
                        "sentenceStartIndex": 0,
                        "sentenceEndIndex": 24,
                        "entityMentions": [
                            {
                                "name": "Barack Obama",
                                "type": "Entity",
                                "label": "PERSON",
                                "startIndex": 0,
                                "endIndex": 11,
                                "iri": "knox-kb01.srv.aau.dk/Barack_Obama"
                            }
                        ]
                    }
                ]
            }
        ]

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"text": "[/INST]'Class': 'Agent'"}]
        }
        mock_post.return_value = mock_response

        # Call the function
        with patch('concept_linking.solutions.PromptEngineering.main.requests') as mock_requests:
            mock_requests.post.return_value = mock_response
            result = main.classify_entity_mentions(input_data, False)

        self.assertTrue(result, expected_result)


    @patch('concept_linking.solutions.PromptEngineering.main.requests.post')
    def test_classify_entity_mentions_unknown(self, mock_post):
        expected_result = [
            (
                "knox-kb01.srv.aau.dk/Barack_Obama",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/unknown"
            )
        ]

        input_data = [
            {
                "fileName": "Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barack Obama is an agent.",
                        "sentenceStartIndex": 0,
                        "sentenceEndIndex": 24,
                        "entityMentions": [
                            {
                                "name": "Barack Obama",
                                "type": "Entity",
                                "label": "PERSON",
                                "startIndex": 0,
                                "endIndex": 11,
                                "iri": "knox-kb01.srv.aau.dk/Barack_Obama"
                            }
                        ]
                    }
                ]
            }
        ]

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"text": "[/INST]'Class': 'Person'"}]
        }
        mock_post.return_value = mock_response

        # Call the function
        with patch('concept_linking.solutions.PromptEngineering.main.requests') as mock_requests:
            mock_requests.post.return_value = mock_response
            result = main.classify_entity_mentions(input_data, False)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
