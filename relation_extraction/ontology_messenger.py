import requests
import re
import os
from dotenv import load_dotenv

from relation_extraction.API_handler import APIHandler

class OntologyMessenger(APIHandler):
    def API_endpoint():
        return "http://knox-proxy01.srv.aau.dk/knox-api/triples"

    def send_request():
        load_dotenv()
        "Function to extract relations based on the specified pattern"
        print("Getting relations from online ontology...")
        relations = []
        query_string_s = 'http://dbpedia.org/ontology/'
        query_string_o = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'
        PARAMS = {"g":"http://knox_ontology", "s": query_string_s, "o": query_string_o}
        HEADERS = {"Access-Authorization": os.getenv("ACCESS_SECRET")}
        r = requests.get(url=OntologyMessenger.API_endpoint(), params=PARAMS, headers=HEADERS)

        data = r.json()

        for triple in data["triples"]:
            relation = re.split("http://dbpedia.org/ontology/", triple["s"]["Value"])[1]
            relations.append(relation)
            
        return relations
