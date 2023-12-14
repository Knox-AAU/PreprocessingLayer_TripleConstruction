# src/text_processing.py
import nltk

# Check if punkt is already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    # Download punkt if not found
    print("Downloading punkt...")
    nltk.download('punkt')
    print("Download complete.")


def basic_tokenization_function(sentence):
    # Tokenize the sentence using nltk
    tokens = nltk.word_tokenize(sentence)

    # You might want to perform additional preprocessing or filtering here

    return tokens
