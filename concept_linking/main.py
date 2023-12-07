import os
from concept_linking.solutions.PromptEngineering.main import perform_entity_type_classification
from concept_linking.solutions.UntrainedSpacy.main import untrainedSpacySolution

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))


def entity_type_classification(input_data):
    msg = "Performing entity type classification using: "
    # Remove the comment sign from the solution you want to run as main in the KNOX Pipeline.

    # String Comparison
    # print(f'{msg} "StringComparison solution"')

    # Untrained Spacy
    #untrainedSpacySolution(input_data)

    # PromptEngineering
    perform_entity_type_classification(input_data)

    # Machine Learning
