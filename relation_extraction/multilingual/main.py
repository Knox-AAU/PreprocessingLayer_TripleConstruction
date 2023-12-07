import json
from relation_extraction.ontology_messenger import OntologyMessenger
from relation_extraction.knowledge_graph_messenger import KnowledgeGraphMessenger
from relation_extraction.multilingual.llm_messenger import LLMMessenger

def parse_data(data):
    "Removes entity mentions with no iri and sentences with less than two entity mentions"

    for file in data:
        for i, sentence in enumerate(file["sentences"]):
            for i, em in enumerate(sentence["entityMentions"]): #remove all entity mentions with iri=null
                if em["iri"] is None:
                    sentence["entityMentions"].pop(i)
            if len(sentence["entityMentions"]) < 2: #skip if less than 2 entity mentions
                file["sentences"].pop(i)
    return data

def begin_relation_extraction(data):
    try:
        relations = OntologyMessenger.send_request()
    except Exception as E:
        print(f"Exception during retrieval of relations: {str(E)}")
        raise Exception(f"Exception during retrieval of relations")
    
    try:
        parsed_data = parse_data(data)
    except Exception as E:
        print(f"Exception during parse of data {str(E)}")
        raise Exception("Incorrectly formatted input. Exception during parsing")
    
    try:
        triples = []
        chunk_size = 650
        split_relations = [relations[i:i + chunk_size] for i in range(0, len(relations), chunk_size)] #Split the relations into lists of size chunk_size
        for split_relation in split_relations:
            triples.extend(LLMMessenger.prompt_llm(parsed_data, split_relation, relations))
    except Exception as E:
        print(f"Exception during prompt to Llama 2: {str(E)}")
        raise Exception("Exception during prompt to Llama 2")

    try:
        KnowledgeGraphMessenger.send_request(triples)
    except Exception as E:
        print(f"Exception during request to database. {str(E)}")
        raise Exception("Data was not sent to database due to connection error")
    
begin_relation_extraction([
    {
        "filename": "path/to/Artikel.txt",
        "language": "en",
        "sentences": [
            {
                "sentence": "Barrack Obama is married to Michelle Obama.",
                "sentenceStartIndex": 20,
                "sentenceEndIndex": 62,
                "entityMentions": 
                [
                    { "name": "Barrack Obama", "startIndex": 0, "endIndex": 12, "iri": "knox-kb01.srv.aau.dk/Barack_Obama" },
                    { "name": "Michelle Obama", "startIndex": 27, "endIndex": 40, "iri": "knox-kb01.srv.aau.dk/Michele_Obama" }
                ]
            }
        ]
    }
]
)