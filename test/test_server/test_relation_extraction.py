import unittest
from unittest import mock
from relation_extraction.NaiveMVP.main import *


class TestHandleRelationPostRequest(unittest.TestCase):
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_relations_fail(self, mock_extract_specific_relations):
        mock_extract_specific_relations.side_effect = Exception()
        data = dict()
        with self.assertRaises(Exception):
            handle_relation_post_request(data)

        mock_extract_specific_relations.assert_called_once()


    @mock.patch('relation_extraction.NaiveMVP.main.parse_data')
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_parse_fail(self, mock_extract_specific_relations, mock_parse_data):
        mock_extract_specific_relations.return_value = []
        mock_parse_data.side_effect = Exception()
        
        data = dict()
        with self.assertRaises(Exception):
            handle_relation_post_request(data)

        mock_extract_specific_relations.assert_called_once()
        mock_parse_data.assert_called_once()


    @mock.patch('relation_extraction.knowledge_graph_messenger.KnowledgeGraphMessenger.send_request')
    @mock.patch('relation_extraction.NaiveMVP.main.parse_data')
    @mock.patch('relation_extraction.ontology_messenger.OntologyMessenger.send_request')
    def test_handle_post_request_raises_exception_if_db_component_fail(self, mock_extract_specific_relations, mock_parse_data, mock_send_to_db):
        mock_extract_specific_relations.return_value = []
        mock_parse_data.return_value = dict()
        mock_send_to_db.side_effect = Exception()
        data = dict()
        with self.assertRaises(Exception):
            handle_relation_post_request(data)

        mock_extract_specific_relations.assert_called_once()
        mock_parse_data.assert_called_once()
        mock_send_to_db.assert_called_once()


class TestFindBestMatch(unittest.TestCase):
    
    def test_find_best_match(self):
        relations = ["test", "relation", "extraction"]
        testdata = [
            {
                "token": "test",
                "expected": "test",
                "similarity": 1
            },
            {
                "token": "relation",
                "expected": "relation",
                "similarity": 1
            },
            {
                "token": "extraction",
                "expected": "extraction",
                "similarity": 1
            },
            {
                "token": "tesr",
                "expected": "test",
                "similarity": 0.75
            }
        ]
        
        for td in testdata:
            res = find_best_match(td["token"], relations)
            self.assertEqual(res["similarity"], td["similarity"])
            self.assertEqual(res["predicted_relation"], td["expected"])


class TestFilterTokens(unittest.TestCase):

    def test_filter_tokens(self):
        testdata = [
            {
                "tokens": ["test", "of", "filter", "tokens"],
                "entity_mentions": [
                    {"name": "test"},
                    {"name": "tokens"}
                ],
                "expected": ["of", "filter"]
            },
            {
                "tokens": ["test", "test", "of", "filter", "tokens"],
                "entity_mentions": [
                    {"name": "test"},
                    {"name": "tokens"}
                ],
                "expected": ["of", "filter"]
            },
            {
                "tokens": ["test", "of", "filter", "tokens"],
                "entity_mentions": [],
                "expected": ["test", "of", "filter", "tokens"]
            }
        ]

        for td in testdata:
            res = filter_tokens(td["tokens"], td["entity_mentions"])

            self.assertEqual(len(res), len(td["expected"]))
            for token in res:
                self.assertTrue(token in td["expected"])
                

class TestFindBestTriple(unittest.TestCase):

    @mock.patch("relation_extraction.NaiveMVP.main.find_best_match")
    @mock.patch("relation_extraction.NaiveMVP.main.filter_tokens")
    def test_find_best_triple(self, mock_filter_tokens, mock_best_match):
        
        relations = ["test", "not", "this"]
        testdata = [
            {
                "sentence": {
                    'sentence': "this is a test sentence", 
                    'tokens': ["this", "is", "a", "sentence"],
                    'entity_mentions': [
                        { "name": "this", "startIndex": 0, "endIndex": 12, "iri": "/this" },
                        { "name": "sentence", "startIndex": 27, "endIndex": 40, "iri": "/sentence" }
                    ]
                },
                "relations": relations,
                "best_match": {'similarity': 1, 'predicted_relation': "test"},
                "expected": ["/this", "test", "/sentence"]
            },
            {
                "sentence": {
                    'sentence': "I am a sentence not to be tested", 
                    'tokens': ['I', 'am', 'a', 'sentence', 'to', 'be', 'tested'],
                    'entity_mentions': [
                        { "name": "I", "startIndex": 0, "endIndex": 12, "iri": "/i" },
                        { "name": "tested", "startIndex": 27, "endIndex": 40, "iri": "/tested" }
                    ]
                },
                "relations": relations,
                "best_match": {'similarity': 1, 'predicted_relation': "not"},
                "expected": ["/i", "not", "/tested"]
            },
            {
                "sentence": {
                    'sentence': "I am a sentence not to be tested", 
                    'tokens': ['I', 'am', 'a', 'sentence', 'not', 'to', 'be', 'tested'],
                    'entity_mentions': [
                        { "name": "I", "startIndex": 0, "endIndex": 12, "iri": "/i" },
                        { "name": "tested", "startIndex": 27, "endIndex": 40, "iri": "/tested" }
                    ]
                },
                "relations": relations,
                "best_match": {'similarity': 0, 'predicted_relation': "what"},
                "expected": ["/i", "---", "/tested"]
            }
        ]

        for td in testdata:
            mock_filter_tokens.return_value = td["sentence"]["tokens"]
            mock_best_match.return_value = td["best_match"]
            res = find_best_triple(td["sentence"], td["relations"])
            self.assertEqual(len(res), 3) #must be triple
            for str in res:
                self.assertTrue(str in td["expected"])

class TestParseData(unittest.TestCase):

    @mock.patch("relation_extraction.NaiveMVP.main.find_best_triple")
    def test_parse_data_removes_ems_without_iri(self, mock_find_best):
        mock_find_best.return_value = ["test", "of", "triple"]
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

        relations = []
        res = parse_data(data, relations)
        mock_find_best.assert_called_with({
                'sentence': "Barrack Obama is married to Michelle Obama and they have a dog.", 
                'tokens': ['Barrack', 'Obama', 'is', 'married', 'to', 'Michelle', 'Obama', 'and', 'they', 'have', 'a', 'dog.'],
                'entity_mentions': [
                    { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                    { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama"}
                ]
            },
            [])
        
        expected_res = ["test", "of", "triple"]
        for i, str in enumerate(res[0]):
            self.assertEqual(str, expected_res[i], f"Got: {res}, expected {expected_res}")

    @mock.patch("relation_extraction.NaiveMVP.main.find_best_triple")
    def test_parse_data_ignores_sentences_with_lt_two_ems(self, mock_find_best):
        mock_find_best.return_value = None
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
                            { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" }
                        ]
                    }
                ]
            }
        ]
        relations = []
        res = parse_data(data, relations)
        self.assertFalse(mock_find_best.called)
        self.assertEqual(len(res), 0)


if __name__ == '__main__':
    unittest.main()
