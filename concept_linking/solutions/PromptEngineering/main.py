import json
import re
import requests
import time
import os
from rdflib import Graph, URIRef
from rdflib.plugins.sparql import prepareQuery
from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger


api_url = "http://127.0.0.1:5000/llama"
headers = {"Content-Type": "application/json"}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


def read_ontology_class():
    return extract_super_classes_from_ontology()


def generate_triples(output_data):
    triples = []
    for sentence_data in output_data["sentences"]:
        for mention in sentence_data["entityMentions"]:
            iri = mention["iri"]
            classification = mention["classification"]
            print(f'GenerateTriples() - Entity: {mention}, Classification: {classification}')

            # Skip creating triples if the classification is "Unknown"
            if classification == "Unknown":
                continue

            # Map the classification to the corresponding DBpedia ontology type
            dbpedia_type = f"http://dbpedia.org/ontology/{classification}"

            triple = [iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_type]
            triples.append(triple)

    return triples


def classify_entity_mentions(input_data):
    start_time = time.time()
    ontology_classes_list = read_ontology_class()
    ontology_classes_string = ", ".join(ontology_classes_list)

    output_data = {"sentences": []}
    max_retries = 3

    # Iterate through each sentence
    for sentence_data in input_data[0]["sentences"]:
        content_sentence = sentence_data["sentence"]

        # Iterate through each entity mention in the sentence
        for mention in sentence_data["entityMentions"]:
            if mention["type"] == "Entity":
                content_entity = mention["name"]
                print(f'Entity to classify: {content_entity}')

                prompt_template = {
                    "system_message": ("The input sentence is all your knowledge. \n"
                                       "Do not answer if it can't be found in the sentence. \n"
                                       "Do not use bullet points. \n"
                                       "Do not identify entity mentions yourself, use the provided ones \n"
                                       "Given the input in the form of the content from a file: \n"
                                       "[Sentence]: {content_sentence} \n"
                                       "[EntityMention]: {content_entity} \n"),

                    "user_message": ("Classify the [EntityMention] in regards to ontology classes: {ontology_classes} \n"
                                     "The output answer must be in JSON in the following format: \n"
                                     "{{ \n"
                                     "'Entity': 'Eiffel Tower', \n"
                                     "'Class': 'ArchitecturalStructure' \n"
                                     "}} \n"),

                    "max_tokens": 4092
                }

                outer_while_retry_count = 0
                while True:  # Run until entity is mapped to a provided ontology class
                    outer_while_retry_count += 1
                    print(f'--- RUN Count #{outer_while_retry_count} (Outer While loop) ---')
                    prompt = {key: value.format(
                        content_sentence=content_sentence,
                        content_entity=content_entity,
                        ontology_classes=ontology_classes_string
                    ) if isinstance(value, str) else value for key, value in prompt_template.items()}

                    inner_while_retry_count = 0
                    result_text = ''
                    # Retrying until we get a not none response
                    while inner_while_retry_count < max_retries:
                        inner_while_retry_count += 1
                        print(f'--- RUN Count #{inner_while_retry_count} (Inner While loop) ---')
                        response = requests.post(api_url, data=json.dumps(prompt), headers=headers)

                        if response.status_code == 200:
                            output = response.json()  # Assuming the response is in JSON format

                            if output["choices"] and output["choices"][0]["text"] not in (None, '.'):
                                result_text = output["choices"][0]["text"]
                                break
                            else:
                                print("Output is null, empty, or contains only a dot. Retrying...")
                                time.sleep(2)
                        else:
                            print(f"Error: {response.status_code} - {response.text}")

                    # Find the index of [/INST]
                    inst_index = result_text.find('[/INST]')

                    # Extract text after [/INST]
                    if inst_index != -1:
                        inst_text = result_text[inst_index + len('[/INST]'):]
                        match = re.search(r"'Class': ['\"](\w+)['\"]", inst_text)
                        classification = match.group(1) if match and match.group(1) in ontology_classes_list else None

                        if classification:
                            print(f'Classification result: {classification}')
                            output_sentence_data = {
                                "sentence": content_sentence,
                                "entityMentions": [
                                    {
                                        "name": mention["name"],
                                        "startIndex": mention["startIndex"],
                                        "endIndex": mention["endIndex"],
                                        "iri": mention["iri"],
                                        "classification": classification
                                    }
                                ]
                            }
                            output_data["sentences"].append(output_sentence_data)
                            break  # Exit the while loop if entity is mapped to a provided ontology class
    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Elapsed time: {elapsed_time} seconds")
    return output_data


# Considering all classes that is a direct subclass of owl:Thing as a root class.
def extract_super_classes_from_ontology():
    g = Graph()
    ontology_file_path = os.path.join(PROJECT_ROOT, "data/files/ontology.ttl")

    g.parse(ontology_file_path, format="ttl")

    # Define RDF namespace prefixes
    rdfs = URIRef("http://www.w3.org/2000/01/rdf-schema#")
    owl = URIRef("http://www.w3.org/2002/07/owl#")

    query_str = """SELECT ?class
    WHERE {
        ?class a owl:Class ;
               rdfs:subClassOf owl:Thing .
    }"""
    query = prepareQuery(query_str, initNs={"rdfs": rdfs, "owl": owl})
    res = g.query(query)
    root_classes = []

    try:
        for row in res:
            class_uri = row['class']
            class_name = class_uri.split("/")[-1]
            root_classes.append(class_name)
    except Exception as e:
        print(e)

    return root_classes


def perform_entity_type_classification(post_json):
    print(f'Running: {post_json}')

    # Classify entity mentions using llama api
    output_data_response = classify_entity_mentions(post_json)

    # Generate triples
    generated_triples = generate_triples(output_data_response)
    try:
        KnowledgeGraphMessenger.send_request(generated_triples)
    except Exception as E:
        print(f"Exception during request to database. {str(E)}")
        raise Exception("Data was not sent to database due to connection error")
