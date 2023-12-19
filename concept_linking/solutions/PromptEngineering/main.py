import json
import re
import requests
import time
import os
from rdflib import Graph, URIRef
from rdflib.plugins.sparql import prepareQuery
from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger
from concept_linking.tools.triple_helper import *

# Local API url python
api_url = "http://127.0.0.1:5000/llama"

# Local API url docker
# api_url = "http://llama-cpu-server:5000/llama"



# Remote API url
# api_url = "http://knox-proxy01.srv.aau.dk/llama-api/llama"

headers = {"Access-Authorization": os.getenv("ACCESS_SECRET"), "Content-Type": "application/json"}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


def read_ontology_class():
    return extract_super_classes_from_ontology()


def classify_entity_mentions(input_data, output_sentence_test_run):
    start_time = time.time()
    ontology_classes_list = read_ontology_class()
    ontology_classes_string = ", ".join(ontology_classes_list)

    max_outer_retries = 5
    max_inner_retries = 3
    triples = []

    entity_mentions_dict = extract_entity_mentions_from_input(input_data)
    # Iterate over each entry in the dictionary
    for sentence_key, entity_mentions in entity_mentions_dict.items():
        content_sentence = sentence_key
        for mention in entity_mentions:
            content_entity = mention[0]
            content_iri = mention[1]
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
            while outer_while_retry_count < max_outer_retries:  # Run until entity is mapped to a provided ontology class
                found_classification = False
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
                while inner_while_retry_count < max_inner_retries:
                    inner_while_retry_count += 1
                    print(f'    --- RUN Count #{inner_while_retry_count} (Inner While loop) ---')
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
                        found_classification = True
                        # Generate triples if an entity was succesfully classified with the ontology
                        if output_sentence_test_run:
                            triples.append({sentence_key: (content_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/ontology/" + classification)})
                        else:
                            triples.append((content_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/ontology/" + classification))

                        break  # Exit the while loop if entity is mapped to a provided ontology class
            if not found_classification:
                if output_sentence_test_run:
                    triples.append({sentence_key: (content_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                                   "http://dbpedia.org/ontology/unknown")})
                else:
                    triples.append((content_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                    "http://dbpedia.org/ontology/unknown"))

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Elapsed time: {elapsed_time} seconds")
    return triples


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


def perform_entity_type_classification(post_json, output_file_path=None, output_sentence_test_run=False):
    msg = "Performing entity type classification using: "
    print(f'{msg} "PromptEngineering solution"')
    if output_file_path is not None:
        print("Running in test mode")

    # Classify entity mentions using llama api
    generated_triples = classify_entity_mentions(post_json, output_sentence_test_run)

    if len(generated_triples) > 0:
        print(f'"Successfully generated {len(generated_triples)} triples"')

        if output_file_path is not None:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(generated_triples, outfile, ensure_ascii=False, indent=4)
        else:
            try:
                KnowledgeGraphMessenger.send_request(generated_triples)
            except Exception as E:
                print(f"Exception during request to database. {str(E)}")
                raise Exception("Data was not sent to database due to connection error")
    else:
        print("No triples generated")


if __name__ == '__main__':
    input_file = os.path.join(PROJECT_ROOT, "data/files/EvaluationData/evaluationSet_EN_small.json")
    output_file = os.path.join(PROJECT_ROOT, "data/files/PromptEngineering/output.json")

    f = open(input_file,  encoding="utf-8")
    data = json.load(f)
    perform_entity_type_classification(data, output_file, True)
