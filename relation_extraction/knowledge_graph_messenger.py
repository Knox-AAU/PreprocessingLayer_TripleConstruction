import requests
import os
from dotenv import load_dotenv

from relation_extraction.API_handler import APIHandler

class KnowledgeGraphMessenger(APIHandler):
    def API_endpoint():
        return "http://knox-proxy01.srv.aau.dk/knox-api/triples"
        
    def send_request(output):
        HEADERS = {"Access-Authorization": os.getenv("ACCESS_SECRET")}
        PARAMS={"g": "http://knox_database"}
        FORMATTED_OUTPUT = KnowledgeGraphMessenger.format_output(output)
        response = requests.post(url=KnowledgeGraphMessenger.API_endpoint(), json=FORMATTED_OUTPUT, params=PARAMS, headers=HEADERS)
        # print(f"db component response: {response.text}")
        return response.text
    
    @classmethod
    def format_output(self, output):
        formatted_output = {"triples": output}
        return formatted_output




