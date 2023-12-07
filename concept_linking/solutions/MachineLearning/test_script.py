import torch
from src.data_preprocessing import load_data, extract_sentences
from src.model_module import ModelClass
from src.config import ModelConfig, TrainingConfig
from src.prediction_dataset import PredictionDataset

#hunginface
# Load your data
test_data = load_data('test/predict_3_classes.json')
test_data = extract_sentences(test_data)

# Create an instance of your model (the same architecture as during training)
model = ModelClass(ModelConfig.input_size,
                   ModelConfig.embedding_dim,
                   ModelConfig.hidden_size,
                   ModelConfig.num_classes)

# Load the trained model
model.load_state_dict(torch.load('3_classes_model.pth'))
model.eval()  # Set the model to evaluation mode

# Create PredictionDataset with the loaded model
prediction_dataset = PredictionDataset(test_data, model)

class_index_to_name = {
    0: 'Person',
    1: 'Place',
    2: 'Organisation'

    # ... add more as needed
}

# Iterate through the dataset and get predictions
for i, data_point in enumerate(prediction_dataset):
    input_indices = data_point['input']
    predicted_class_index = data_point['predicted_class']
    predicted_class = data_point['predicted_class']
    predicted_class_name = class_index_to_name.get(predicted_class_index, 'Unknown')
    print(f"Sentence number: {i+1}, Predicted Class: {predicted_class_name}")