# src/model_training.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from concept_linking.solutions.MachineLearning.src.training_dataset import TrainingDataset
from concept_linking.solutions.MachineLearning.src.model_module import ModelClass
from concept_linking.solutions.MachineLearning.src.config import TrainingConfig, ModelConfig


def custom_collate(batch):
    # Separate inputs, targets, and lengths
    #inputs = [torch.LongTensor(item['input']) for item in batch]
    #targets = [torch.tensor(item['target'], dtype=torch.float32) for item in batch]
    #lengths = [item['length'] for item in batch]
    inputs = [torch.LongTensor(item['input']) for item in batch]
    targets = [item['target'].clone().detach() for item in batch]
    lengths = [item['length'] for item in batch]

    # Pad sequences
    inputs_padded = pad_sequence(inputs, batch_first=True, padding_value=0)

    # If there are multiple target labels for a sample, stack them into a 2D tensor
    targets_padded = pad_sequence(targets, batch_first=True, padding_value=0)

    return {'input': inputs_padded, 'target': targets_padded, 'length': lengths}

def train_model(train_data, val_data, model_name, model=None, config=TrainingConfig):
    # Instantiate your dataset class for training and validation
    possible_labels = ['Person', 'Place', 'Organisation']
    train_dataset = TrainingDataset(train_data, possible_labels)
    val_dataset = TrainingDataset(val_data, possible_labels)

    # Create DataLoader instances for training and validation
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True, collate_fn=custom_collate)
    val_loader = DataLoader(val_dataset, batch_size=config.batch_size, collate_fn=custom_collate)

    # If model is not provided, instantiate a new model
    if model is None:
        model = ModelClass(ModelConfig.input_size, ModelConfig.embedding_dim, ModelConfig.hidden_size, ModelConfig.num_classes)
    else:
        # Load the existing model's state dictionary
        model.load_state_dict(torch.load(model_name))

    # Define loss function and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

    # Training loop
    for epoch in range(config.num_epochs):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            # Extract inputs, targets, and lengths from the batch
            inputs, targets, lengths = batch['input'], batch['target'], batch['length']

            # Convert targets to a tensor
            targets = torch.tensor(targets, dtype=torch.float32)

            # Convert inputs to a tensor
            inputs = torch.tensor(inputs)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(inputs, lengths)

            # Compute the loss
            loss = criterion(outputs, targets)

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        # Calculate average training loss for the epoch
        avg_train_loss = total_loss / len(train_loader)

        # Validation loop
        model.eval()
        val_loss = 0.0

        with torch.no_grad():
            for batch in val_loader:
                # Extract inputs and targets from the batch
                inputs, targets, lengths = batch['input'], batch['target'], batch['length']

                # Convert inputs to a tensor
                inputs = torch.tensor(inputs)

                # Forward pass
                outputs = model(inputs, lengths)

                # Compute the loss
                loss = criterion(outputs, targets)

                val_loss += loss.item()

        # Calculate average validation loss for the epoch
        avg_val_loss = val_loss / len(val_loader)

        # Print training progress
        print(f'Epoch {epoch+1}/{config.num_epochs} => Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}')

    # Save the updated trained model
    torch.save(model.state_dict(), model_name)

    return model
