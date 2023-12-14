import json


def calculate_metrics(data):
    TP = 0
    FP = 0
    FN = 0
    data_without_duplicates = data

    for triples in data_without_duplicates["multilingual"]["triples"]:
        triples["triples_from_solution"] = set(tuple(triple) for triple in triples["triples_from_solution"])
        triples["triples_from_solution"] = list(list(triple) for triple in triples["triples_from_solution"])

    for element in data_without_duplicates["multilingual"]["triples"]:
        TP += element["contains_hits"]
        FP += len(element["triples_from_solution"]) - element["contains_hits"]
        FN += len(element["expected_triples"]) - element["contains_hits"]

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    F1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    return {"precision": precision, "recall": recall, "F1_score": F1}

def main():
    with open("relation_extraction/Evaluation/evaluation_results.json") as f:
        res_obj = json.load(f)

    print(calculate_metrics(res_obj))

main()