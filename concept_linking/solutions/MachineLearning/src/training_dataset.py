import torch
from torch.utils.data import Dataset
from concept_linking.solutions.MachineLearning.src.text_processing import basic_tokenization_function

def preprocess_sentence(sentence):
    processed_sentences = [basic_tokenization_function(sentence)]
    return processed_sentences

def obtain_target_labels(entry, class_to_index):
    # Extract target labels from the entry
    target_labels = [mention['classification'] for mention in entry['entityMentions']]

    # Convert string labels to integer indices using the provided class_to_index mapping
    target_indices = [class_to_index.setdefault(label, len(class_to_index)) for label in target_labels]

    # Return the integer indices directly
    return target_indices

class TrainingDataset(Dataset):
    def __init__(self, data, possible_labels):
        self.data = data
        self.num_classes = len(possible_labels)
        self.class_to_index = {label: idx for idx, label in enumerate(possible_labels)}  # Initialize class_to_index
        self.possible_labels = possible_labels
        self.build_vocab()

    def build_vocab(self):
        # Extract all words and classes from your data
        all_words = [word for entry in self.data for sentence in preprocess_sentence(entry.get('sentence', [])) for word
                     in sentence]

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

        # Process sentences to obtain input data (e.g., tokenization)
        input_data = preprocess_sentence(sentence)

        # Flatten the list of sentences
        input_data = [word for sentence in input_data for word in sentence]
        # Convert words to indices
        input_indices = self.words_to_indices(input_data)

        # Extract target labels
        target_labels = obtain_target_labels(entry, self.class_to_index)

        # Convert target labels to tensor
        target_tensor = torch.zeros(len(self.class_to_index))
        target_tensor[target_labels] = 1

        return {'input': input_indices, 'target': target_tensor, 'length': len(input_indices)}
