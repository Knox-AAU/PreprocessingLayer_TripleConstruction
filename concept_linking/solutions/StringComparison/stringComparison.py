from .utils import writeFile, translateWordToEn, similar
from rdflib import Graph

ontology_path = "../concept_linking/data/files/ontology.ttl"
ontology_datatypes_path = "../../data/documents/ontology_datatypes.txt"
ontology_classes_path = "../../data/documents/ontology_classes.txt"
ontology_classes_multilingual_path = "../../concept_linking/data/documents/ontology_classes_multilingual.txt"



def generateOntologyDatatypes():
    g = Graph()
    g.parse(ontology_path, format="ttl")

    # TODO: Get all datatype properties from ontology.
    query = """
        SELECT DISTINCT ?datatype
        WHERE {
            ?datatype a rdfs:Datatype .
        }
    """

    result = g.query(query)

    # Collect datatype properties in an array and set them to lowercase. Then save to file.
    datatype_properties_lc = [
        str(row.datatype).removeprefix("http://dbpedia.org/datatype/")
        for row in result
    ]

    # Save to file using the provided writeFile function
    writeFile(ontology_datatypes_path, "\n".join(datatype_properties_lc))


def generateOntologyClasses():
    g = Graph()
    g.parse(ontology_path, format="ttl")

    # se om ontology og spacy classerne er de samme, hvis nej print listen for dem
    query = """
        SELECT DISTINCT ?class
        WHERE {
            ?class a owl:Class .
        }
    """

    results = g.query(query)
    ontology_classes = [str(result["class"]) for result in results]

    # Collect ontology classes in array and sets it to lower case. Then saves to file.
    ontology_classesLC = []
    for ontology_class in ontology_classes:
        ontology_classesLC.append(
            ontology_class.removeprefix("http://dbpedia.org/ontology/")
        )
    writeFile(ontology_classes_path, "\n".join(ontology_classesLC))


def queryLabels():
    g = Graph()
    g.parse(ontology_path, format="ttl")

    #find labels på alle klasser
    qres = g.query("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?class (lang(?label) as ?language) ?label
    WHERE {
        ?class a owl:Class .
        ?class rdfs:label ?label .
    } 
    """)

    classesDict = {}
    for row in qres:
        r = str(row).split()

        #prov:Revision i ontology bliver til provRevision. Hvad er prov?
        className = "".join(c for c in r[0] if c.isalpha()).removeprefix("rdflibtermURIRefhttpdbpediaorgontology")
        labelLang = "".join(c for c in r[1] if c.isalpha()).removeprefix("rdflibtermLiteral")
        label = "".join(c for c in r[2] if c.isalpha()).removeprefix("rdflibtermLiteral")
        if className not in classesDict:
            classesDict[className] = []
        classesDict[className].append({labelLang: label})
    
    with open(ontology_classes_multilingual_path, 'w') as f:
       for key, value in classesDict.items():
          f.write(f'{key}: {value}\n')
    return classesDict


def generateTriples(JSONObject, classesDict):
    triples = []
    for object in JSONObject:
        language = object["language"]
        ontologyLanguage = "en"
        for sentence in object['sentences']:
            ems = sentence['entityMentions']
            filtered_ems = [em for em in sentence.get('entityMentions', []) if em.get('type') == 'Entity']
            sentence = sentence['sentence']
            new_sent = sentence

            ems_indices = []
            for em in ems:
                ems_indices.append((em['startIndex'], em['endIndex']))

            #sletter de ord i sætningen, der er EMs
            for start_index, end_index in reversed(ems_indices):
                new_sent = new_sent[:start_index] + new_sent[end_index+2:]
            
            new_sent = new_sent.removesuffix(".")
            words = new_sent.split(" ")

            matchingWords = [] #words der findes i ontologyen
            SIMILARITY_REQ = 0.9 #minimumkrav til string similarity.

            if language == ontologyLanguage:
                matchingWords = findEnMatches(words, classesDict, SIMILARITY_REQ)
            else:
                matchingWords = findNonEnMatches(words, classesDict, SIMILARITY_REQ, language)
 
            for word in matchingWords:
                for em in filtered_ems:
                    triples.append({sentence: [em['iri'], "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/ontology/" + word['className']]})
    return triples


# For hvert ord, check om det matcher et engelsk label på een af vores dict classer med minimin SIMILARITY_REQ. Hvis ja, tilføj til matchingWords.
def findEnMatches(words, classesDict, SIMILARITY_REQ):
    matchingWords = []
    for word in words:
        for className, labelsList in classesDict.items():
            for label_dict in labelsList:
                if 'en' in label_dict and similar(word.lower(), label_dict['en'].lower()) >= SIMILARITY_REQ:
                    matchingWords.append({'className': className, 'label': word})
                    break
    return matchingWords


# Samme som findEnMatches, men tjekker efter et label match på originalsproget. Hvis der ikke findes et label på
# sproget, så oversætter vi og leder efter et passende engelsk label.
def findNonEnMatches(words, classesDict, SIMILARITY_REQ, language):
    translatedWords = []
    matchingWords = []
    for word in words:
        translatedWords.append(translateWordToEn(word, language))

    for i, word in enumerate(words):
                for className, labelsList in classesDict.items():
                    for label_dict in labelsList:
                        if language in label_dict and similar(word.lower(), label_dict[language].lower()) >= SIMILARITY_REQ:
                            matchingWords.append({'className': className, 'label': word})
                            break  
                        elif 'en' in label_dict and similar(translatedWords[i].lower(), label_dict['en'].lower()) >= SIMILARITY_REQ:
                            matchingWords.append({'className': className, 'label': word})
                            break
    return matchingWords
