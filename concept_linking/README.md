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




## Authors
- Caspar Emil Jensen <ceje22@student.aau.dk>
- Gamma Ishimwe Ntakiyimana <gntaki22@student.aau.dk>
- Lucas Pedersen <llhp21@student.aau.dk>
- Mikkel Wissing <mwissi21@student.aau.dk>
- Rune Eberhardt <reber21@student.aau.dk>
- Vi Thien Le <vle21@student.aau.dk>
