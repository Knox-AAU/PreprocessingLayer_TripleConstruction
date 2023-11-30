import requests
import re

from relation_extraction.API_handler import APIHandler

class OntologyMessenger(APIHandler):
    def API_endpoint():
        return "http://130.225.57.13/knox-api/triples"

    def send_request():
        "Function to extract relations based on the specified pattern"
        print("Getting relations from online ontology...")
        relations = []
        query_string_s = 'http://dbpedia.org/ontology/'
        query_string_o = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'
        PARAMS = {"g":"http://knox_ontology", "s": query_string_s, "o": query_string_o}
        HEADERS = {"Access-Authorization":"internal_key"}
        r = requests.get(url=OntologyMessenger.API_endpoint(), params=PARAMS, headers=HEADERS)
        print(f"db component response: {r.text}")

        data = r.json()

        for triple in data["triples"]:
            relation = re.split("http://dbpedia.org/ontology/", triple["s"]["Value"])[1]
            relations.append(relation)
            
        return relations

if __name__ == "__main__":
    OntologyMessenger.send_request()