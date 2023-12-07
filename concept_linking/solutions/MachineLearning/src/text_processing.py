# src/text_processing.py
import nltk

# Download the nltk punkt tokenizer data (run this once)
nltk.download('punkt')


def basic_tokenization_function(sentence):
    # Tokenize the sentence using nltk
    tokens = nltk.word_tokenize(sentence)

    # You might want to perform additional preprocessing or filtering here

    return tokens
