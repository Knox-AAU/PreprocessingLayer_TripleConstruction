import json
import os
from concept_linking.solutions.UntrainedSpacy.untrainedSpacy import *
from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


def generateTXTfiles():
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()


def untrainedSpacySolution(post_json, output_file_path=None, output_sentence_test_run=False):
    msg = "Performing entity type classification using: "
    print(f'{msg} "UntrainedSpacy solution"')
    if output_file_path is not None:
        print("Running in test mode")

    generated_triples = generateTriplesFromJSON(post_json, output_sentence_test_run)
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
    output_file = os.path.join(PROJECT_ROOT, "data/files/UntrainedSpacy/output.json")
    f = open(input_file,  encoding="utf-8")
    data = json.load(f)
    untrainedSpacySolution(data, output_file, True)
