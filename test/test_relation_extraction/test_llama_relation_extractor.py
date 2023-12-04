import unittest
from unittest import mock
from relation_extraction.multilingual.main import *

class TestHandleRelationPostRequest(unittest.TestCase):
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_relations_fail(self, mock_extract_specific_relations):
        mock_extract_specific_relations.side_effect = Exception()
        data = dict()
        with self.assertRaises(Exception):
            begin_relation_extraction(data)

        mock_extract_specific_relations.assert_called_once()
    
    @mock.patch('relation_extraction.multilingual.main.parse_data')
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_parse_fail(self, mock_extract_specific_relations, mock_parse_data):
        mock_extract_specific_relations.return_value = []
        mock_parse_data.side_effect = Exception()

        data = dict()
        with self.assertRaises(Exception):
            begin_relation_extraction(data)
        
        mock_extract_specific_relations.assert_called_once()
        mock_parse_data.assert_called_once()

    @mock.patch('relation_extraction.multilingual.llm_messenger.LLMMessenger.prompt_llm')
    @mock.patch('relation_extraction.multilingual.main.parse_data')
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_prompt_llm_fail(self, mock_extract_specific_relations, mock_parse_data, mock_prompt_llm):
        mock_extract_specific_relations.return_value = []
        mock_parse_data.return_value = []
        mock_prompt_llm.side_effect = Exception()

        data = dict()
        with self.assertRaises(Exception):
            begin_relation_extraction(data)
        
        mock_extract_specific_relations.assert_called_once()
        mock_parse_data.assert_called_once()
        mock_prompt_llm.assert_called_once()

    @mock.patch('relation_extraction.knowledge_graph_messenger.KnowledgeGraphMessenger.send_request')    
    @mock.patch('relation_extraction.multilingual.llm_messenger.LLMMessenger.prompt_llm')
    @mock.patch('relation_extraction.multilingual.main.parse_data')
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_send_to_db_fail(self, mock_extract_specific_relations, mock_parse_data, mock_prompt_llm, mock_send_to_db):
        mock_extract_specific_relations.return_value = []
        mock_parse_data.return_value = []
        mock_prompt_llm.return_value = {}
        mock_send_to_db.side_effect = Exception()

        data = dict()
        with self.assertRaises(Exception):
            begin_relation_extraction(data)
        
        mock_extract_specific_relations.assert_called_once()
        mock_parse_data.assert_called_once()
        mock_prompt_llm.assert_called_once()
        mock_send_to_db.assert_called_once()

class TestParseData(unittest.TestCase):
    def test_parse_remove_ems_without_iri(self):
        data = [
            {
                "filename": "path/to/Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barrack Obama is married to Michelle Obama and they have a dog.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": 
                        [
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                            { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama"},
                            { "name": "Dog", "startIndex": 27, "endIndex": 40, "iri": None}
                        ]
                    }
                ]
            }
        ]
        res = parse_data(data)

        expected = [
            {
                "filename": "path/to/Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barrack Obama is married to Michelle Obama and they have a dog.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": 
                        [
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                            { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama"},
                        ]
                    }
                ]
            }
        ]

        self.assertEqual(res, expected)

    def test_parse_remove_sentences_with_lt_two_ems(self):
        data = [
            {
                "filename": "path/to/Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barrack Obama is married to Michelle Obama and they have a dog.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": 
                        [
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                        ]
                    },
                    {
                        "sentence": "Barrack Obama is married to Michelle Obama and they have a dog.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": 
                        [
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                            { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama"},
                        ]
                    }
                ]
            }
        ]
        res = parse_data(data)

        expected = [
            {
                "filename": "path/to/Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Barrack Obama is married to Michelle Obama and they have a dog.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": 
                        [
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                            { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama"},
                        ]
                    }
                ]
            }
        ]

        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
