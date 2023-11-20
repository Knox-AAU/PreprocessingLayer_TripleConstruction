import json
import strsimpy
import sys
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from output import format_output
from getRel import extract_specific_relations
import datetime
import multiprocessing as mp
from functools import partial

ontology_file_path = 'DBpedia_Ont.ttl'
threshold = 0
normalized_levenshtein = NormalizedLevenshtein()


def find_best_match(token, relations):
    "Finds the best match given a token and a set of relations"
    best_relation_match = ""
    highest_similarity = 0
    dt = datetime.datetime.now()
    for relation in relations:
        similarity = normalized_levenshtein.similarity(token, relation)
        highest_similarity = similarity if similarity > highest_similarity else highest_similarity
        best_relation_match = relation if similarity == highest_similarity else best_relation_match
    # print(f"find_best_match: {(datetime.datetime.now()-dt).total_seconds()}")
    return {'similarity': highest_similarity, 'predicted_relation': best_relation_match}

def filter_tokens(tokens, entity_mentions):
    "Filters out tokens that are substrings of the entity mentions"

    filtered_tokens = []

    for entity_mention in entity_mentions:
        for token in tokens:
            if token not in entity_mention["name"]:
                filtered_tokens.append(token)

    return filtered_tokens

def find_best_triple(sentence, relations):
    "Finds the best triple by comparing each token in a sentence to every relation and returning the triple where the similarity was highest"
    entity_mentions = sentence["entity_mentions"]
    dt = datetime.datetime.now()
    filtered_tokens = filter_tokens(sentence["tokens"], entity_mentions)
    #print(f"filter_tokens: {(datetime.datetime.now()-dt).total_seconds()}")
    best_triple = []
    highest_similarity = 0
    dt = datetime.datetime.now()
    for token in filtered_tokens:
        result = find_best_match(token, relations)
        if result["similarity"] > highest_similarity and result["similarity"] > threshold: #Only supporting 2 entity mentions per sentence
            highest_similarity = result["similarity"]
            best_triple = [entity_mentions[0]["name"], result["predicted_relation"], entity_mentions[1]["name"]]
    if highest_similarity == 0:
        best_triple = [entity_mentions[0]["name"], "---",entity_mentions[1]["name"]]
    #print(f"handle all tokens: {(datetime.datetime.now()-dt).total_seconds()}")
    return best_triple

def parse_data(data, relations):
    "Parses JSON data and converts it into a dictionary with information on sentence, tokens, and entity mentions"
    output = []
    for file in data:
        file_name = file["fileName"]
        sentences_in_data = file["sentences"]

        for sentence_object in sentences_in_data:
            tokens = sentence_object["sentence"].split(" ")
            entity_mentions = sentence_object["entityMentions"]
            
            sentence = {
                'sentence': sentence_object["sentence"], 
                'tokens': tokens,
                'entity_mentions': entity_mentions
            }
            
            output.append(find_best_triple(sentence, relations))
            
    return output

def main():
    relations = extract_specific_relations(ontology_file_path)
    # Opening JSON file
    with open('relation_extraction/inputSentences.json', 'r') as f:
        # returns JSON object as a dictionary 
        data = json.load(f)
    format_output(parse_data(data, relations))

if __name__ == "__main__":
    main()
