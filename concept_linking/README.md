# Concept Linking

---
## Background
In group D, four different solutions have been implemented. These will be mentioned further in a later section.
At default the solution that will be running is PromptEngineering.

To change which solution to run in the pipeline perform the following changes...

First change directory to the 'server' folder in the root directory.

Next, open the server.py file.
On line 24, under the text "#Begin ConceptLinking"
Change the code, to run the desired solution.


## Requirements
For any of the four solutions, it is necessary to install the requirements found
in the requirements.txt file inside /{Solution_Name}/requirements.txt

However since this is a joint codebase for both relation-extraction and concept-linking,
there is a global requirements.txt file in the root directory.
It follows a nested structure, meaning that installing only to one if the root folder, 
will install all the rest.

It will install both the necessary requirements for both groups' solutions.
However since it is possible to change which of the four concept-linking solutions to run, 
it is also necessary to the requirements to be installed accordingly.
This is done by navigation to

```
./concept_linking/requirements.txt
```
In this file, there is listed a reference to the four different requirements.txt files.
Remove the #(comment) from the one referencing the solution you want to run.

### Example
Install the requirements for the PromptEngineering solution

Navigate to the following directory

```
../concept_linking/solutions/PromptEngineering/
```

And run the following command
```
pip install -r requirements.txt
```

## Solutions

Following below is brief description of each of the four solutions and how to get started.

---


### Machine Learning
description WIP

### Prompt Engineering
Uses the LLM Llama2. A prompt is given to the model. 

```
 prompt_template = {
                    "system_message": ("The input sentence is all your knowledge. \n"
                                       "Do not answer if it can't be found in the sentence. \n"
                                       "Do not use bullet points. \n"
                                       "Do not identify entity mentions yourself, use the provided ones \n"
                                       "Given the input in the form of the content from a file: \n"
                                       "[Sentence]: {content_sentence} \n"
                                       "[EntityMention]: {content_entity} \n"),

                    "user_message": ("Classify the [EntityMention] in regards to ontology classes: {ontology_classes} \n"
                                     "The output answer must be in JSON in the following format: \n"
                                     "{{ \n"
                                     "'Entity': 'Eiffel Tower', \n"
                                     "'Class': 'ArchitecturalStructure' \n"
                                     "}} \n"),

                    "max_tokens": 4092
                }
```

The variables {content_sentence} and {content_entity} is found in a previous part of the KNOX pipeline.
The variable {ontology_classes} fetched by the Ontology endpoint provided by group E(Database Layer)


#### Using LocalLlama API server
It is possible to use a local LlamaServer. It can be found in ../concept_linking/tools/LlamaServer.
A README for setting up an instance of this server can be found in the directory given above.

#### Using the Llama API server hosted in the KNOX pipeline
WIP
Go to the directory /concept_linking/PromptEngineering/main
set the api_url accordingly
``` 
api_url={domain or ip+port of llama server hosted in the knox pipeline}
```
Refer to the <a href="https://docs.google.com/spreadsheets/d/1dvVQSEvw15ulNER8qvl1P8Ufq-p3vLU0PswUeahhThg/edit#gid=0" target="_blank">Server Distribution document</a>
 for specific dns and ip+port information.

### String Comparison
description WIP


### Untrained Spacy
description WIP



---

## Tools

### LlamaServer

### OntologyGraphBuilder

---

## Report
Description of the project can be found in the report on Overleaf (requires permission)

## Authors
Lucas, Gamma, Vi, Mikkel, Caspar & Rune