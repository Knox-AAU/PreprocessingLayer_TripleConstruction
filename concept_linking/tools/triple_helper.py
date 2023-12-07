def extract_entity_mentions_from_input(input_data):
    entity_mentions_by_sentence = {}

    # Iterate through each sentence
    for sentence_data in input_data[0]["sentences"]:
        sentence = sentence_data["sentence"]
        entity_mentions = []

        # Iterate through each entity mention in the sentence
        for entity_mention in sentence_data["entityMentions"]:
            if entity_mention["type"] == "Entity":
                em_name = entity_mention["name"]
                em_iri = entity_mention["iri"]
                em_label = entity_mention["label"].lower()
                entity_mentions.append((em_name, em_iri, em_label))

        # Add the entity mentions to the dictionary
        entity_mentions_by_sentence[sentence] = entity_mentions
    return entity_mentions_by_sentence

