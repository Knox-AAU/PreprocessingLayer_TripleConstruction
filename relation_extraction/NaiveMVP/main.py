import json
from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger
import strsimpy
import sys
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from relation_extraction.ontology_messenger import OntologyMessenger
import datetime
import multiprocessing as mp
from functools import partial

threshold = 0
normalized_levenshtein = NormalizedLevenshtein()


def find_best_match(token, relations):
    "Finds the best match given a token and a set of relations"
    best_relation_match = ""
    highest_similarity = 0
    for relation in relations:
        similarity = normalized_levenshtein.similarity(token, relation)
        highest_similarity = similarity if similarity > highest_similarity else highest_similarity
        best_relation_match = relation if similarity == highest_similarity else best_relation_match
    
    return {'similarity': highest_similarity, 'predicted_relation': best_relation_match}

def filter_tokens(tokens, entity_mentions):
    "Filters out tokens that are substrings of the entity mentions"
    ems = [em["name"] for em in entity_mentions]
    return [token for token in tokens if token not in ems] 

def find_best_triple(sentence, relations):
    "Finds the best triple by comparing each token in a sentence to every relation and returning the triple where the similarity was highest"
    entity_mentions = sentence["entity_mentions"]
    filtered_tokens = filter_tokens(sentence["tokens"], entity_mentions)
    best_triple = []
    highest_similarity = 0
    for token in filtered_tokens:
        result = find_best_match(token, relations)
        if result["similarity"] > highest_similarity and result["similarity"] > threshold: #Only supporting 2 entity mentions per sentence
            highest_similarity = result["similarity"]
            best_triple = [entity_mentions[0]["iri"], result["predicted_relation"], entity_mentions[1]["iri"]]
    if highest_similarity == 0:
        best_triple = [entity_mentions[0]["iri"], "---",entity_mentions[1]["iri"]]
    return best_triple

def parse_data(data, relations):
    "Parses JSON data and converts it into a dictionary with information on sentence, tokens, and entity mentions"
    output = []
    for file in data:
        sentences_in_data = file["sentences"]

        for sentence_object in sentences_in_data:
            for i, em in enumerate(sentence_object["entityMentions"]):  #remove all entity mentions with iri=null
                if em["iri"] is None:
                    sentence_object["entityMentions"].pop(i)
                    print(f"Removed entity because iri=null: {em}")
            if len(sentence_object["entityMentions"]) < 2: #skip if less than 2 entity mentions
                continue
            tokens = sentence_object["sentence"].split(" ")
            entity_mentions = sentence_object["entityMentions"]
            
            sentence = {
                'sentence': sentence_object["sentence"], 
                'tokens': tokens,
                'entity_mentions': entity_mentions
            }
            
            output.append([elem.replace(" ","_") for elem in find_best_triple(sentence, relations)])
            
    return output

def handle_relation_post_request(data):
    try:
        relations = OntologyMessenger.send_request()
    except Exception as E:
        print(f"Exception during retrieval of relations: {str(E)}")
        raise Exception(f"Exception during retrieval of relations")
    
    try:
        parsed_data = parse_data(data, relations)
    except Exception as E:
        print(f"Exception during parse of data {str(E)}")
        raise Exception("Incorrectly formatted input. Exception during parsing")
    
    try:
        KnowledgeGraphMessenger.send_request(parsed_data)
    except Exception as E:
        print(f"Exception during request to database. {str(E)}")
        raise Exception("Data was not sent to database due to connection error")


def main():
    relations = OntologyMessenger.send_request()
    # Opening JSON file
    with open('inputSentences.json', 'r') as f:
        # returns JSON object as a dictionary 
        data = json.load(f)
    KnowledgeGraphMessenger.send_request(parse_data(data, relations))

if __name__ == "__main__":
    main()
