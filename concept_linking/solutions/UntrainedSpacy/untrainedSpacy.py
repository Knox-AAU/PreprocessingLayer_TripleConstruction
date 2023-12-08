import spacy
from concept_linking.solutions.UntrainedSpacy.utils import clearFile, appendFile, writeFile, readFile
from concept_linking.tools.triple_helper import *


nlp = spacy.load("en_core_web_lg")
nlp_da = spacy.load("da_core_news_lg")

spacy_label_path = "../../documents/spacy_labels.txt"
ontology_classes_path = "../../data/documents/ontology_classes.txt"
spacy_matched_path = "../../data/documents/spacy_matched.txt"
spacy_unmatched_path = "../../data/documents/spacy_unmatched.txt"
spacy_explanations_path = "../../data/documents/spacy_explanations.txt"


def generateSpacyLabels():
    # Collect spaCy labels in list and sets it to lower case. Then saves to file.
    spacy_labelsLC = []
    spacy_labels = nlp.get_pipe("ner").labels
    for label in spacy_labels:
        spacy_labelsLC.append(label.lower())
    # writeFile(spacy_label_path, "\n".join(spacy_labelsLC))


def generateSpacyMatches():
    # Compare ontology and spacy labels
    matched_labels = []
    unmatched_labels = []

    spacy_labels = readFile(spacy_label_path).splitlines()
    ontology_classes = readFile(ontology_classes_path).splitlines()

    for label in spacy_labels:
        for ontology_class in ontology_classes:
            if label == ontology_class:
                matched_labels.append(label)
        if label != matched_labels[-1]:
            unmatched_labels.append(label)

    # writeFile(spacy_matched_path, "\n".join(matched_labels))
    # writeFile(spacy_unmatched_path, "\n".join(unmatched_labels))


def generateSpacyUnmatchedExplanations():
    # Generates a file with a little explanation for each of the unmatched spaCy labels
    clearFile(spacy_explanations_path)

    unmatched_labels = readFile(spacy_unmatched_path).splitlines()
    for unmatched in unmatched_labels:
        appendFile(
            spacy_explanations_path,
            "".join(unmatched + ": " + spacy.explain(unmatched.upper())) + "\n",
        )


def generateTriplesFromJSON(input_data, output_sentence_test_run):
    """
        Generates triples from entity mentions in sentences based on spaCy and ontology classes.

        Parameters:
        - json_object: JSON object containing sentences with entity mentions.

        Returns:
        - list: List of triples (subject, predicate, object).
    """
    triples = []

    # matches the spaCy labels to the ontology classes 
    labels_dict = {
        "event": "https://dbpedia.org/ontology/Event",
        "fac": "https://dbpedia.org/ontology/Building",
        "gpe": "https://dbpedia.org/ontology/Country",
        "language": "https://dbpedia.org/ontology/Language",
        "law": "https://dbpedia.org/ontology/Law",
        "loc": "https://dbpedia.org/ontology/Location",
        "norp": "https://dbpedia.org/ontology/Group",
        "org": "https://dbpedia.org/ontology/Organisation",
        "product": "https://www.w3.org/2002/07/owl#/thing",
        "work_of_art": "https://dbpedia.org/ontology/Artwork",
        "person": "https://dbpedia.org/ontology/Person",
        "per": "https://dbpedia.org/ontology/Person", 
        "misc": "https://www.w3.org/2002/07/owl#/thing"
        
    }

    entity_mentions_dict = extract_entity_mentions_from_input(input_data)
    # Iterate over each entry in the dictionary
    for sentence_key, entity_mentions in entity_mentions_dict.items():
        for entity_mention in entity_mentions:
            em_iri = entity_mention[1]
            em_label = entity_mention[2]
            # Trying to retrieve the URI with a specific label (first param), if none exists, set to unknown.
            dbpedia_uri = labels_dict.get(em_label, "https://dbpedia.org/ontology/unknown")
            # Generate triples
            if output_sentence_test_run:
                triples.append({sentence_key: (em_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_uri)})
            else:
                triples.append((em_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_uri))

    return triples
                        