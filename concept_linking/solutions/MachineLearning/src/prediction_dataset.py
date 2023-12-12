import torch
from torch.utils.data import Dataset
from concept_linking.solutions.MachineLearning.src.text_processing import basic_tokenization_function


def preprocess_sentence(sentence):
    print("Input sentence:", sentence)  # Add this line to check the input sentence
    processed_sentences = basic_tokenization_function(sentence)
    return processed_sentences


class PredictionDataset(Dataset):
    def __init__(self, data, model):
        self.data = data
        self.model = model
        self.word_to_index = None  # Initialize to None
        self.build_vocab()

    def build_vocab(self):
        # Extract all words and classes from your data
        all_words = [word for entry in self.data for sentence in entry.get('sentence', []) for word in sentence]

        # Create a set to get unique words
        unique_words = set(all_words)

        # Create a vocabulary mapping each word to an index
        self.word_to_index = {word: idx for idx, word in enumerate(unique_words)}

    def words_to_indices(self, words):
        # Use your vocabulary to map words to indices
        indices = [self.word_to_index[word] for word in words]
        return indices

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        entry = self.data[index]

        # Extract relevant information from the entry
        sentence = entry.get('sentence', [])

        # Convert words to indices
        input_indices = self.words_to_indices(sentence)

        # Use your trained model to predict the classification
        with torch.no_grad():
            model_input = torch.tensor(input_indices, dtype=torch.long).unsqueeze(0)  # Assuming batch size 1
            # Assuming lengths is the length of the input sequence
            lengths = torch.tensor([len(input_indices)])
            model_output = self.model(model_input, lengths)

        # Convert the model's output to probabilities or class labels as needed
        # You might need to adjust this based on your model's architecture and output format
        predicted_class = torch.argmax(model_output).item()

        return {'input': input_indices, 'predicted_class': predicted_class, 'length': len(input_indices)}