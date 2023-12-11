import unittest
from concept_linking.solutions.StringComparison.stringComparison import generateTriples, queryLabels, findEnMatches, \
    findNonEnMatches
from concept_linking.solutions.StringComparison.utils import similar


class GenerateTriplesTest(unittest.TestCase):
    def test_generate_triples_true(self):
        test_data = [
            {
                "fileName": "Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Martin Kjær is a person and has a car",
                        "sentenceStartIndex": 0,
                        "sentenceEndIndex": 149,
                        "entityMentions": [
                            {
                                "name": "Martin Kjær",
                                "type": "Entity",
                                "label": "PERSON",
                                "startIndex": 0,
                                "endIndex": 10,
                                "iri": "knox-kb01.srv.aau.dk/Martin_Kjær"
                            },
                        ]
                    },
                ]
            }]

        ont_types = queryLabels()

        result = generateTriples(test_data, ont_types, False)

        expected_result = [
            (
                "knox-kb01.srv.aau.dk/Martin_Kjær",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/Person"
            ),
            (
                "knox-kb01.srv.aau.dk/Martin_Kjær",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/PersonFunction"
            )
        ]

        self.assertEqual(result, expected_result)

    def test_generate_triples_false(self):
        test_data = [
            {
                "fileName": "Artikel.txt",
                "language": "en",
                "sentences": [
                    {
                        "sentence": "Martin Kjær is a person and has a car",
                        "sentenceStartIndex": 0,
                        "sentenceEndIndex": 149,
                        "entityMentions": [
                            {
                                "name": "Martin Kjær",
                                "type": "Entity",
                                "label": "PERSON",
                                "startIndex": 0,
                                "endIndex": 10,
                                "iri": "knox-kb01.srv.aau.dk/Martin_Kjær"
                            },
                        ]
                    },
                ]
            }]

        ont_types = queryLabels()

        result = generateTriples(test_data, ont_types, False)

        expected_result = [
            (
                "knox-kb01.srv.aau.dk/Martin",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/Organization"
            ),
            (
                "knox-kb01.srv.aau.dk/Martin",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                "http://dbpedia.org/ontology/Place"
            )
        ]

        self.assertNotEqual(result, expected_result)


class SimilarTest(unittest.TestCase):
    def test_identical_strings(self):
        self.assertEqual(similar("hello", "hello"), 1.0)
        self.assertNotEqual(similar("hello", "hello"), 0)

    def test_different_strings(self):
        self.assertLess(similar("hello", "world"), 0.5)

    def test_partial_similarity(self):
        self.assertAlmostEqual(similar("abc", "ab"), 0.8, places=1)

    def test_case_insensitivity(self):
        self.assertEqual(similar("HELLO", "hello"), 1.0)

    def test_empty_strings(self):
        self.assertEqual(similar("", ""), 1.0)

    def test_high_similarity_z_and_s_words(self):
        self.assertGreater(similar("Organization", "Organisation"), 0.9)


class FindEmMatchesTest(unittest.TestCase):
    def test_find_em_matches_true(self):
        text = "Martin Kjær is a person and has a car"
        words = text.split(" ")  # ['Martin', 'Kjær', 'is', 'a', 'person', 'and', 'has', 'a', 'car']
        similarity_req = 0.9
        classes_dict = queryLabels()
        matching_words = findEnMatches(words, classes_dict,
                                       similarity_req)  # [{'className': 'Person', 'label': 'person'}, {'className': 'PersonFunction', 'label': 'person'}]

        expected_matching_words = [
            {
                'className': 'Person',
                'label': 'person'
            },
            {
                'className': 'PersonFunction',
                'label': 'person'
            }
        ]

        self.assertEqual(matching_words, expected_matching_words)

    def test_find_em_matches_false(self):
        text = "Martin Kjær is a person and has a car"
        words = text.split(" ")  # ['Martin', 'Kjær', 'is', 'a', 'person', 'and', 'has', 'a', 'car']
        similarity_req = 0.9
        classes_dict = queryLabels()
        matching_words = findEnMatches(words, classes_dict,
                                       similarity_req)  # [{'className': 'Person', 'label': 'person'}, {'className': 'PersonFunction', 'label': 'person'}]

        expected_matching_words = [
            {
                'className': 'Person',
                'label': 'organisation'
            },
            {
                'className': 'PersonFunction',
                'label': 'organisation'
            }
        ]

        self.assertNotEqual(matching_words, expected_matching_words)

"""
class FindNonEmMatchesTest(unittest.TestCase):
    def test_find_non_em_matches_true(self):
        text = "Martin Kjær er person og har en bil"
        words = text.split(" ")
        similarity_req = 0.9
        classes_dict = queryLabels()
        language = "da"
        matching_words = findNonEnMatches(words, classes_dict,
                                          similarity_req,
                                          language)

        expected_matching_words = [
            {
                'className': 'Person',
                'label': 'person'
            },
            {
                'className': 'PersonFunction',
                'label': 'person'
            }
        ]

        self.assertEqual(matching_words, expected_matching_words)

    def test_find_non_em_matches_false(self):
        text = "Martin Kjær er person og har en bil"
        words = text.split(" ")
        similarity_req = 0.9
        classes_dict = queryLabels()
        language = "da"
        matching_words = findNonEnMatches(words, classes_dict,
                                          similarity_req,
                                          language)

        expected_matching_words = [
            {
                'className': 'Person',
                'label': 'organisation'
            },
            {
                'className': 'PersonFunction',
                'label': 'organistaion'
            }
        ]

        self.assertNotEqual(matching_words, expected_matching_words)
"""

if __name__ == '__main__':
    unittest.main()
