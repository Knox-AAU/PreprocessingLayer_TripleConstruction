import unittest
from unittest.mock import patch, MagicMock
from concept_linking.solutions.UntrainedSpacy.untrainedSpacy import generateSpacyLabels, generateSpacyMatches, generateSpacyUnmatchedExplanations, generateTriplesFromJSON

class TestUntrainedSpacyFunctions(unittest.TestCase):
    class TestGenerateTriplesFromJSON(unittest.TestCase):

        @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.extract_entity_mentions_from_input')
        def test_generateTriplesFromJSON(self, entity_mentions):
            # Mocking the extract_entity_mentions_from_input function
            entity_mentions.return_value = {
                "sentence1": [
                    ("knox-kb01.srv.aau.dk/Bob_Marley", "person")
                ]
            }

            test_data = [
                {
                    "fileName": "Artikel.txt",
                    "language": "en",
                    "sentences": [
                        {
                            "sentence": "Bob Marley is a person and has a car",
                            "sentenceStartIndex": 0,
                            "sentenceEndIndex": 149,
                            "entityMentions": [
                                {
                                    "name": "Bob Marley",
                                    "type": "Entity",
                                    "label": "PERSON",
                                    "startIndex": 0,
                                    "endIndex": 10,
                                    "iri": "knox-kb01.srv.aau.dk/Bob Marley"
                                },
                            ]
                        },
                    ]
                }
            ]

            output_sentence_test_run = False

            expected_triples = [
                ("knox-kb01.srv.aau.dk/Bob_Marley", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                 "https://dbpedia.org/ontology/Person")
            ]

            result = generateTriplesFromJSON(test_data, output_sentence_test_run)
            self.assertEqual(result, expected_triples)

    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.writeFile')
    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.nlp.get_pipe')
    def test_generateSpacyLabels(self, mock_get_pipe, mock_writeFile):
        mock_get_pipe.return_value.labels = ['PERSON', 'ORG']
        generateSpacyLabels()

    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.readFile')
    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.writeFile')
    def test_generateSpacyMatches(self, mock_writeFile, mock_readFile):
        mock_readFile.side_effect = ['person\norg', 'person\ncompany']
        generateSpacyMatches()

    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.readFile')
    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.appendFile')
    @patch('concept_linking.solutions.UntrainedSpacy.untrainedSpacy.clearFile')
    def test_generateSpacyUnmatchedExplanations(self, mock_clearFile, mock_readFile, mock_appendFile):
        mock_readFile.return_value = 'org'
        generateSpacyUnmatchedExplanations()

if __name__ == '__main__':
    unittest.main()