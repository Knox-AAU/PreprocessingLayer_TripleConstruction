import os
from concept_linking.solutions.PromptEngineering.main import perform_entity_type_classification
from concept_linking.solutions.UntrainedSpacy.main import untrainedSpacySolution
from concept_linking.solutions.StringComparison.main import stringComparisonSolution
from concept_linking.solutions.MachineLearning.main import predict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))


def entity_type_classification(input_data):
    # Remove the comment sign from the solution you want to run as main in the KNOX Pipeline.

    # String Comparison
    #stringComparisonSolution(input_data)

    # Untrained Spacy
    untrainedSpacySolution(input_data)

    # PromptEngineering
    #perform_entity_type_classification(input_data)

    # Machine Learning
    #predict(input_data)

