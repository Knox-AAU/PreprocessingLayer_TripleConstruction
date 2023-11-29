import requests
import re

# def extract_specific_relations(ontology_file_path):
#     "Function to extract relations based on the specified pattern"
#     relations = set()
#     with open(ontology_file_path, 'r', encoding='utf-8', errors='ignore') as file:
#         lines = file.readlines()
#         i = 0
#         for i, line in enumerate(lines):
#             line = line.strip()
#             # Check if the line starts with a colon and the next lines contain the specified pattern
#             if line.startswith(":") and i+1 < len(lines) and "a rdf:Property, owl:ObjectProperty ;" in lines[i+1]:
#                 relation = line.split()[0]  # Extracting the relation name
#                 relation = relation[1:] # Remove colon
#                 relations.add(relation)
#             i += 1
            
#     return sorted(relations) 

def extract_specific_relations():
    "Function to extract relations based on the specified pattern"
    relations = []
    URL = "http://130.225.57.13/knox-api/triples"
    query_string_s = 'http://dbpedia.org/ontology/'
    query_string_o = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'
    PARAMS = {"g":"http://knox_ontology", "s": query_string_s, "o": query_string_o}
    HEADERS = {"Access-Authorization":"internal_key"}
    r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
    print(f"db component response: {r.text}")

    data = r.json()

    for triple in data["triples"]:
        relation = re.split("http://dbpedia.org/ontology/", triple["s"]["Value"])[1]
        relations.append(relation)
        
    return relations

extract_specific_relations()