import os
from concept_linking.tools.Evaluation.Evaluation import evaluate_dataset, read_scores_from_json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


if __name__ == "__main__":
    name_of_result = "String_DK"
    json_file_path = os.path.join(PROJECT_ROOT, "data/files/EvaluationData/Results/" + name_of_result + ".json")

    scores = read_scores_from_json(json_file_path)
    evaluate_dataset(scores)
