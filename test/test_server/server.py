
import unittest
import requests
from http.server import HTTPServer
from threading import Thread, Lock
from server.server import PreProcessingHandler
import json



VALID_POST_STRING = """[
    {
        "fileName": "Artikel.txt",
        "language": "en",
        "sentences": [
            {
                "sentence": "Since the sudden exit of the controversial CEO Martin Kjær last week, both he and the executive board in Region North Jutland have been in hiding.",
                "sentenceStartIndex": 0,
                "sentenceEndIndex": 148,
                "entityMentions": [
                    {
                        "name": "last week",
                        "type": "Literal",
                        "label": "DATE",
                        "startIndex": 59,
                        "endIndex": 68,
                        "iri": null
                    },
                    {
                        "name": "Martin Kjær",
                        "type": "Entity",
                        "label": "PERSON",
                        "startIndex": 47,
                        "endIndex": 58,
                        "iri": "knox-kb01.srv.aau.dk/Martin_Kjær"
                    },
                    {
                        "name": "Region North Jutland",
                        "type": "Entity",
                        "label": "LOC",
                        "startIndex": 105,
                        "endIndex": 125,
                        "iri": "knox-kb01.srv.aau.dk/Region_North_Jutland"
                    }
                ]
            }
        ]
    }
]
            """
INVALID_POST_STRING = """
[{{}}]
"""

PORT = 4201
lock = Lock()

class TestServerEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        lock.acquire()
        self.server_thread = Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    @classmethod
    def start_server(self):
        self.server = HTTPServer(('localhost', PORT), PreProcessingHandler)
        lock.release()
        self.server.serve_forever()

    @classmethod
    def tearDownClass(self):
        self.server.shutdown()
        self.server.server_close()

    def test_pre_processing_endpoint_with_valid_data(self):
        while(lock.locked()):
            pass

        dictionary = json.loads(VALID_POST_STRING)
        response = requests.post(f'http://localhost:{PORT}/tripleconstruction', json=dictionary)
        self.assertEqual(response.status_code, 200)

    def test_pre_processing_endpoint_with_invalid_data_returns_422(self):
        while(lock.locked()):
            pass
        response = requests.post(f'http://localhost:{PORT}/tripleconstruction', json=INVALID_POST_STRING)
        self.assertEqual(response.status_code, 422)
        

if __name__ == '__main__':
    unittest.main()
