
import unittest
import requests
from http.server import HTTPServer
from threading import Thread, Lock
from server.server import PreProcessingHandler
import json



VALID_POST_STRING = """[
                    {
                        "filename": "path/to/Artikel.txt",
                        "language": "en",
                        "sentences": [
                            {
                                "sentence": "Barrack Obama is married to Michelle Obama.",
                                "sentenceStartIndex": 20,
                                "sentenceEndIndex": 62,
                                "entityMentions": 
                                [
                                    { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                                    { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama" }
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
    def setUpClass(cls):
        lock.acquire()
        cls.server_thread = Thread(target=cls.start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def start_server(cls):
        cls.server = HTTPServer(('localhost', PORT), PreProcessingHandler)
        lock.release()
        cls.server.serve_forever()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

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
