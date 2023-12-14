import json
from sklearn.model_selection import train_test_split


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def extract_sentences(data):
    # Extract the 'sentences' key from each document in the data
    return [sentence for entry in data for sentence in entry.get('sentences', [])]


def split_data(data, test_size=0.15, val_size=0.5, random_state=42):
    sentences = extract_sentences(data)

    # Perform the train-test split on the extracted sentences
    train_data, temp_data = train_test_split(sentences, test_size=test_size, random_state=random_state)

    # Check if there are enough samples left for validation
    if len(temp_data) < 2:
        raise ValueError("Not enough samples remaining for validation. Adjust test_size or add more data.")

    val_data, test_data = train_test_split(temp_data, test_size=val_size, random_state=random_state)

    return train_data, val_data, test_data