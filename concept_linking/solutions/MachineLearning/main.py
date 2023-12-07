# main.py
from src.data_preprocessing import load_data, split_data
from src.model_training import train_model
from src.model_module import ModelClass
from src.config import ModelConfig, TrainingConfig


# Load your data
data = load_data('data/generated_data.json')

# Split the data
train_data, val_data, test_data = split_data(data)

# Create an instance of your model
model_instance = ModelClass(ModelConfig.input_size, ModelConfig.embedding_dim, ModelConfig.hidden_size, ModelConfig.num_classes)
model = ModelClass(ModelConfig.input_size,
                   ModelConfig.embedding_dim,
                   ModelConfig.hidden_size,
                   ModelConfig.num_classes)

# Train the model
trained_model = train_model(train_data, val_data, model=model_instance, config=TrainingConfig)
