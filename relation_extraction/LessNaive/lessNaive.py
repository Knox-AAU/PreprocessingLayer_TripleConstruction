from .openie import POST_corenlp
import json
import sys 

import urllib.parse
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from rapidfuzz.distance import Levenshtein
from relation_extraction.output import format_output
from relation_extraction.get_relations import extract_specific_relations


def find_best_ontology_match(api_relation, ontology_relations):
    api_relation = api_relation.lower().replace(" ", "")
    best_ontology_match = ""
    highest_similarity = 0

    for ontology_relation in ontology_relations:
        # similarity = NormalizedLevenshtein().similarity(api_relation.lower(), ontology_relation.lower())
        similarity = Levenshtein.normalized_similarity(api_relation.lower(), ontology_relation.lower(), weights=(1,1,4))
        highest_similarity = similarity if similarity > highest_similarity else highest_similarity
        best_ontology_match = ontology_relation if similarity == highest_similarity else best_ontology_match

    return best_ontology_match


def find_ontology_relations(relations, sentences):
    for urlsentence, sentence in sentences.items():
        sentence["relations"] = []
        for triple in sentence["openie"]:
            valid_entity_mentions = [em["name"] for em in sentence["entityMentions"]]
            if triple["subject"] in valid_entity_mentions and triple["object"] in valid_entity_mentions:
                #subject and object fround by corenlp is same as group B
                sentence["relations"].append({
                    "subject": triple["subject"],
                    "relation": find_best_ontology_match(triple["relation"], relations), #needs to map to closest macth in ontology
                    "object": triple["object"]
                    })
            else:
                print(f"subject '{triple['subject']}' and objcet '{triple['object']}' not found in ems:{valid_entity_mentions}")

def reconstruct_sentence_from_tokens(tokens):
    reconstructed_sentence = ""

    for i, t in enumerate(tokens):
        if i+1 < len(tokens) and t["characterOffsetEnd"] == tokens[i + 1]["characterOffsetBegin"]:
            reconstructed_sentence += t["originalText"]
        elif i+1 < len(tokens) and t["characterOffsetEnd"] != tokens[i + 1]["characterOffsetBegin"]:
            reconstructed_sentence += t["originalText"] + " "
        else:
            reconstructed_sentence += t["originalText"]

    return reconstructed_sentence

def do_relation_extraction(data, ontology_relations):
    sentences = {}
    for f in data:
        for s in f["sentences"]:
            sentences[urllib.parse.quote(s["sentence"])] = s

    openie = json.loads(POST_corenlp(list(sentences.keys())))
    for sentence in openie["sentences"]:
        reconstructed_sentence = reconstruct_sentence_from_tokens(sentence["tokens"])
        sentences[urllib.parse.quote(reconstructed_sentence)]["openie"] = sentence["openie"]

    find_ontology_relations(ontology_relations, sentences)
    relations = []
    for key, val in sentences.items():
        relations.extend(val["relations"])

    tuples = [[r["subject"], r["relation"], r["object"]] for r in relations]
    format_output(tuples)
    return tuples

def main():
    ontology_relations = extract_specific_relations()
    do_relation_extraction(json.load(open("inputSentences.json")), ontology_relations)   
    

if __name__ == "__main__":
    main()

