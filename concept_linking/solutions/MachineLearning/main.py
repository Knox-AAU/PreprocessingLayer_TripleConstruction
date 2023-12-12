from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger
from concept_linking.solutions.MachineLearning.src.prediction_dataset import PredictionDataset
from concept_linking.solutions.MachineLearning.src.data_preprocessing import load_data, split_data, extract_sentences
from concept_linking.solutions.MachineLearning.src.model_training import train_model
from concept_linking.solutions.MachineLearning.src.model_module import ModelClass
from concept_linking.solutions.MachineLearning.src.config import ModelConfig, TrainingConfig

import json
import os
import torch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


def train(create_new_model=False, model_name="model.pth"):
    # Load your data
    training_data = load_data('generate_dataset/generated_data.json')

    # Split the data
    train_data, val_data, test_data = split_data(training_data)

    model = ModelClass(ModelConfig.input_size,
                       ModelConfig.embedding_dim,
                       ModelConfig.hidden_size,
                       ModelConfig.num_classes)

    # Train the model
    if create_new_model:
        trained_model = train_model(train_data, val_data, model_name, model=None, config=TrainingConfig)
    else:
        trained_model = train_model(train_data, val_data, model_name, model=model, config=TrainingConfig)


def predict(input_file_path, output_file_path=None, model_name="model.pth"):
    # Load data
    data = load_data(input_file_path)
    sentences = extract_sentences(data)


    # Create an instance of your model (the same architecture as during training)
    model = ModelClass(ModelConfig.input_size,
                       ModelConfig.embedding_dim,
                       ModelConfig.hidden_size,
                       ModelConfig.num_classes)

    # Load the trained model
    model.load_state_dict(torch.load(model_name))
    model.eval()  # Set the model to evaluation mode

    # Create PredictionDataset with the loaded model
    print("Predicting...")
    prediction_dataset = PredictionDataset(sentences, model)

    class_index_to_name = {
        0: 'Person',
        1: 'Place',
        2: 'Organisation'
    }

    triples = []
    # Iterate through the dataset and get predictions
    for i, data_point in enumerate(prediction_dataset):
        sentence_data = sentences[i]
        entity_mentions = sentence_data.get('entityMentions', [])

        for mention in entity_mentions:
            if mention['type'] == 'Entity':
                # Get the relevant information
                iri = mention.get('iri', 'Unknown')
                predicted_class_index = data_point['predicted_class']
                predicted_class_name = class_index_to_name.get(predicted_class_index, 'Unknown')

                # Create the triple and add it to the list
                #triple = (iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/ontology/" + predicted_class_name)

                # Triples with sentences:
                triple = { sentence_data.get('sentence', 'Unknown'): (iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/ontology/" + predicted_class_name)}
                triples.append(triple)

    if len(triples) > 0:
        print(f'"Successfully generated {len(triples)} triples"')

        if output_file_path is not None:
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(triples, outfile, ensure_ascii=False, indent=4)
        else:
            try:
                KnowledgeGraphMessenger.send_request(triples)
            except Exception as E:
                print(f"Exception during request to database. {str(E)}")
                raise Exception("Data was not sent to database due to connection error")
    else:
        print("No triples generated")


if __name__ == '__main__':
    input_file = os.path.join(PROJECT_ROOT, "data/files/EvaluationData/evaluationSet_DK.json")
    output_file = os.path.join(PROJECT_ROOT, "data/files/MachineLearning/output.json")

    #ONLY IF YOU WANT TO TRAIN FIRST. Adjust training params in src.config.py
    #train(create_new_model=False, model_name="model.pth")

    predict(input_file, output_file, model_name="model.pth")
