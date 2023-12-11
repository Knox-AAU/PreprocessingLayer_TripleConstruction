from stringComparison import *
import json

input_file = "../../data/files/EvaluationData/evaluationSet_EN.json"
output_file = "../../data/files/EvaluationData/output.json"

f = open(input_file,  encoding="utf-8")
data = json.load(f)

data = [
  {
    "fileName": "Artikel.txt",
    "language": "en",
    "sentences": [
      {
        "sentence": "Martin Kjær is a person and has a car",
        "sentenceStartIndex": 0,
        "sentenceEndIndex": 149,
        "entityMentions": [
          {
            "name": "Martin Kjær",
            "type": "Entity",
            "label": "PERSON",
            "startIndex": 0,
            "endIndex": 10,
            "iri": "knox-kb01.srv.aau.dk/Martin_Kjær"
          },
        ]
      },
    ]
  }]

def generateTXTfiles():
    generateOntologyClasses()
    generateOntologyDatatypes()

def stringComparisonSolution():
    ontTypes = queryLabels()
    triples = generateTriples(data, ontTypes)
    if len(triples) > 0:
        print("Successfully generated triples")
    # Convert the array to a JSON string
    writeFile(output_file, json.dumps(triples))


if __name__== '__main__':
    stringComparisonSolution()

