import sys
import xml.etree.ElementTree as ET
from relation_extraction.LessNaive.lessNaive import do_relation_extraction
from relation_extraction.NaiveMVP.main import parse_data
import re
from relation_extraction.get_relations import extract_specific_relations
import datetime
import json


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 3, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()


def convert_testdata_to_input_format():
    objs = []
    tree = ET.parse('relation_extraction/Evaluation/testdataMini.xml')
    root = tree.getroot()
    for entry in root.findall('.//entry'):
        sentence = entry.findall('lex')[0].text
        triples = []
        for otriple in entry.findall("modifiedtripleset/mtriple"):
            triple_string = re.sub(r'\([^)]*\)', '', otriple.text.replace("_", " "))
            triple = tuple(list(map(lambda x: x.strip(), triple_string.split("|"))))
            triples.append(triple)

        objs.append({
            "sentence": sentence,
            "triples": triples
        })
    return objs

def calculate_metrics(data):
    TP = 0
    FP = 0
    FN = 0

    for element in data["triples"]:
        TP += element["contains_hits"]
        FP += len(element["triples_from_solution"]) - element["contains_hits"]
        FN += len(element["expected_triples"]) - element["contains_hits"]

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    F1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    return {"precision": precision, "recall": recall, "F1_score": F1}

def main():
    input_objs = convert_testdata_to_input_format()
    print("testdata converted successfully")
    ontology_relations = extract_specific_relations()
    
    
    solutions_to_test = {
        # "less_naive": do_relation_extraction
        "naive": parse_data
    }
    evaluation_results = dict() #dictionary to hold results of tests
    for name, solution in solutions_to_test.items():
        print(f"Running solution {name}")
        evaluation_result_triples = []
        total_triples = 0
        hits = 0
        dt = datetime.datetime.now()
        printProgressBar(0, len(input_objs), prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i, obj in enumerate(input_objs):
            sentence = obj["sentence"]
            expected_triples = obj["triples"]
            total_triples += len(expected_triples)
            ems = []
            for j, triple in enumerate(expected_triples):
                ems.append(triple[0])
                ems.append(triple[2])
                expected_triples[j] = [expected_triples[j][0].replace(" ", "_"), expected_triples[j][1], expected_triples[j][2].replace(" ", "_")]
            
            ems = list(dict.fromkeys(ems)) #remove duplicate ems

            entity_mentions = [{ "name": em, "startIndex": 0, "endIndex": 0, "iri": em.replace(" ", "_") } for em in ems]    
            input_obj = [{
                "fileName": "path/to/Artikel.txt",
                "sentences": [
                    {
                        "sentence": sentence,
                        "entityMentions": entity_mentions
                    },
                ]
            }]
            
            res = solution(input_obj, ontology_relations)
            res_hits = 0
            for triple in res:
                if triple in expected_triples:
                    res_hits += 1
                    hits +=1

            evaluation_result_triples.append({"sentence":sentence, "triples_from_solution": res, "expected_triples": expected_triples, "contains_hits": res_hits})
            eta = round((((datetime.datetime.now()-dt).total_seconds()/60)/((i+1)/len(input_objs)))*(1-((i+1)/len(input_objs))),5)
            progress_suffix = f"Complete. Timeusage: {round((datetime.datetime.now()-dt).total_seconds()/60,5)} minutes. Eta {eta} minutes."
            printProgressBar(i + 1, len(input_objs), prefix = 'Progress:', suffix = progress_suffix, length = 50)
        
        print(f"Solution {name} finished. Hit {hits}/{total_triples}. Hit percentage: {(hits/total_triples)*100}%")
        evaluation_results[name] = {
            "triples": evaluation_result_triples,
            "result": {"total_expected_triples": total_triples, "hits": hits, "hit_percentage": hits/total_triples},
            "score": calculate_metrics({"triples": evaluation_result_triples})
        }
        
    with open("relation_extraction/Evaluation/evaluation_results.json", "w") as f:
        json.dump(evaluation_results, f, indent=4)
        



if __name__ == "__main__":
    main()