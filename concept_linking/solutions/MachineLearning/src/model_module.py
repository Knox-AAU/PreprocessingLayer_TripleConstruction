import torch
import torch.nn as nn


class ModelClass(nn.Module):
    def __init__(self, input_size, embedding_dim, hidden_size, num_classes):
        super(ModelClass, self).__init__()

        # Use the provided parameters to set hyperparameters
        self.embedding_layer = nn.Embedding(input_size, embedding_dim)
        self.rnn_layer = nn.LSTM(embedding_dim, hidden_size, batch_first=True)
        self.fc_layer = nn.Linear(hidden_size, num_classes)

    def forward(self, x, lengths):
        # Forward pass through the layers
        embedded = self.embedding_layer(x)

        # Pack padded sequence
        packed_input = nn.utils.rnn.pack_padded_sequence(embedded, lengths, batch_first=True, enforce_sorted=False)

        output, _ = self.rnn_layer(packed_input)

        # Unpack the packed sequence
        output, _ = nn.utils.rnn.pad_packed_sequence(output, batch_first=True)

        # Assuming you want to use the output from the last time step
        output = self.fc_layer(output[:, -1, :])

        # Apply sigmoid activation
        output = torch.sigmoid(output)

        return output
