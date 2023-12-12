import unittest
from unittest import mock
from relation_extraction.multilingual.llm_messenger import *

class TestProcessMessage(unittest.TestCase):
    #Needs testing
    def test_send_request(self):
        testdata = [
            {
                
            }
        ]

    def test_process_message(self):
        testdata = [
            {
                "choices": [
                    {
                        "text":'[INST] Barack Obama is married to Michelle Obama. [/INST] In this sentence the triples are: <"Barack Obama", married, "Michelle Obama"> and <"Michelle Obama", married, "Barack Obama">'
                    }
                ],
                "expected": [
                    {
                        "0":"Barack Obama",
                        "1":"married",
                        "2":"Michelle Obama"
                    },
                    {
                        "0":"Michelle Obama",
                        "1":"married",
                        "2":"Barack Obama"
                    }
                ]
            },
            {
                "choices": [
                    {
                        "text":'[INST] Peter and Marianne has the same mother. [/INST] In this sentence the triples are: <"Peter", sibling, "Marianne"> and <"Marianne", sibling, "Peter">'
                    }
                ],
                "expected":[
                    {
                        "0":"Peter",
                        "1":"sibling",
                        "2":"Marianne"
                    },
                    {
                        "0":"Marianne",
                        "1":"sibling",
                        "2":"Peter"
                    }
                ]
            }
        ]

        for td in testdata:
            res = LLMMessenger.process_message(td)
            self.assertEqual(res, td["expected"])

    def test_process_message_wrong_format(self):
        testdata = [
            {
                "choices": [
                    {
                        "text":"[INST] Barack Obama is married to Michelle Obama. [/INST] In this sentence the triples are: Subject: Barack Obama\n Relation: married\n Object: Michelle Obama"
                    }
                ],
                "expected": []
            },
            {
                "choices": [
                    {
                        "text":"[INST] Peter and Marianne has the same mother. [/INST] In this sentence the triples are: Subject: Peter\n Relation: sibling\n Object: Marianne"
                    }
                ],
                "expected":[]
            }
        ]

        for td in testdata:
            res = LLMMessenger.process_message(td)
            self.assertEqual(res, td["expected"])

    def test_check_validity_of_response(self):
        relations = ["married", "sibling", "child", "parent"]
        testdata = [
            {
                "Sentence": {
                    "sentence": "Barack Obama is married to Michelle Obama.",
                    "sentenceStartIndex": 20,
                    "sentenceEndIndex": 62,
                    "entityMentions": 
                    [
                        { "name": "Barack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                        { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michelle_Obama" }
                    ]
                },
                "response": [
                    {
                        "0":"Barack Obama",
                        "1":"married",
                        "2":"Michelle Obama"
                    },
                    {
                        "0":"Michelle Obama",
                        "1":"married",
                        "2":"Barack Obama"
                    }
                ],
                "expected": [
                    [
                        "knox-kb01.srv.aau.dk/Barack_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Michelle_Obama"
                    ],
                    [
                        "knox-kb01.srv.aau.dk/Michelle_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Barack_Obama"
                    ],
                ]
            }
        ]

        for td in testdata:
            res = LLMMessenger.check_validity_of_response(td["Sentence"], td["response"], relations)
            self.assertEqual(res, td["expected"])
    
    @mock.patch("relation_extraction.multilingual.llm_messenger.LLMMessenger.send_request")
    @mock.patch("relation_extraction.multilingual.llm_messenger.LLMMessenger.process_message")
    @mock.patch("relation_extraction.multilingual.llm_messenger.LLMMessenger.check_validity_of_response")
    def test_prompt_llm(self, mock_check_validity, mock_process_message, mock_send_request):
        relations = ["married", "sibling", "child", "parent"]
        split_relations = [["married", "sibling", "child", "parent"]]
        testdata = [
            {
                "response": {
                    "choices": [
                        {
                            "text":'[INST] Barack Obama is married to Michelle Obama. [/INST] In this sentence the triples are: <"Barack Obama", married, "Michelle Obama"> and <"Michelle Obama", married, "Barack Obama">'
                        }
                    ],
                },
                "process_response": [
                    {
                        "0":"Barack Obama",
                        "1":"married",
                        "2":"Michelle Obama"
                    },
                    {
                        "0":"Michelle Obama",
                        "1":"married",
                        "2":"Barack Obama"
                    }
                ],
                "validity_response": [
                    [
                        "knox-kb01.srv.aau.dk/Barack_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Michelle_Obama"
                    ],
                    [
                        "knox-kb01.srv.aau.dk/Michelle_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Barack_Obama"
                    ],
                ],
                "expected": [
                    [
                        "knox-kb01.srv.aau.dk/Barack_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Michelle_Obama"
                    ],
                    [
                        "knox-kb01.srv.aau.dk/Michelle_Obama",
                        "http://dbpedia.org/ontology/married",
                        "knox-kb01.srv.aau.dk/Barack_Obama"
                    ],
                ],
                "data": [
                    {
                        "language": "en",
                        "metadataId":"790261e8-b8ec-4801-9cbd-00263bcc666d",
                        "sentences": [
                            {
                                "sentence": "Barack Obama is married to Michelle Obama.",
                                "sentenceStartIndex": 20,
                                "sentenceEndIndex": 62,
                                "entityMentions": 
                                [
                                    { "name": "Barack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                                    { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michelle_Obama" }
                                ]
                            }
                        ]
                    }
                ],
                "split_relations": split_relations,
                "relations": relations
            }
        ]
        
        for td in testdata:
            mock_send_request.return_value = td["response"]
            mock_process_message.return_value = td["process_response"]
            mock_check_validity.return_value = td["validity_response"]
            res = []
            for split_relation in td["split_relations"]:
                res.extend(LLMMessenger.prompt_llm(td["data"], split_relation, td["relations"]))
            for triple in res:
                self.assertEqual(len(triple), 3) #All must be triples
            self.assertEqual(td["expected"], res)


    def test_API_endpoint(self):
        self.assertEqual(LLMMessenger.API_endpoint(), "http://knox-proxy01.srv.aau.dk/llama-api/llama")


    @mock.patch("os.getenv")
    @mock.patch("requests.post")
    def test_send_request(self, mock_post, mock_getenv):
        mock_post.return_value = "response"
        mock_getenv.return_value = "secret"

        self.assertEqual(LLMMessenger.send_request({"body": "requestbody"}), "response")

