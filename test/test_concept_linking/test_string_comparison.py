import unittest
from concept_linking.solutions.StringComparison.stringComparison import generateTriples, queryLabels
from concept_linking.solutions.StringComparison.utils import similar


class GenerateTriplesTest(unittest.TestCase):
    def test_generate_triples(self):
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

        result = generateTriples(test_data, ont_types)

        expected_result = [
            {
                "Martin Kj\u00e6r is a person and has a car":
                    [
                        "knox-kb01.srv.aau.dk/Martin_Kj\u00e6r",
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                        "http://dbpedia.org/ontology/Person"
                    ]
            },
            {
                "Martin Kj\u00e6r is a person and has a car": [
                    "knox-kb01.srv.aau.dk/Martin_Kj\u00e6r",
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                    "http://dbpedia.org/ontology/PersonFunction"
                ]
            }
        ]

        self.assertEqual(result, expected_result)


class SimilarTest(unittest.TestCase):
    def test_identical_strings(self):
        self.assertEqual(similar("hello", "hello"), 1.0)

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


if __name__ == '__main__':
    unittest.main()
