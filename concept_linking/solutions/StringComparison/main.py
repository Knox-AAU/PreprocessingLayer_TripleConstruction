from stringComparison import *
import json

input_file = "../../data/files/EvaluationData/evaluationSet_EN.json"
output_file = "../../data/files/EvaluationData/output.json"

f = open(input_file,  encoding="utf-8")
data = json.load(f)

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

