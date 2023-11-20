# PreprocessingLayer_TripleConstruction
A repository for groups C (Relation Extraction) and D (Concept Linking) | KNOX 2023

PreprocessingLayer TripleConstruction is responsible for creating triples that can be utilised by group E to construct a knowledge graph.
The triples will be data stored in the form of a subject (entity IRI), predicate, and object (entity IRI), where the subject has some relation to the object. 

## Configuration management 
The solution utilises docker to fetch the latest updates that have been pushed to GitHub.

### Workflow for building and deploying the docker image
Every time something is pushed to main a new docker image will be build. 
```yml
name: Docker deploy image

on: 
  push:
    branches-ignore:
      - "*" # Ignore all branches
      - "!main" # Except main
  workflow_dispatch:

env:
  # Use docker.io for Docker Hub if empty
  REGISTRY: ghcr.io
  # github.repository as <account>/<repo>
  IMAGE_NAME: ${{ github.repository }}

jobs: 
  docker_deploy_image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@28218f9b04b4f3f62068d7b6ce6ca5b26e35336c
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@98669ae865ea3cffbcbaa878cf57c20bbf1c6c38
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
      - name: Build and push Docker image
        uses: docker/build-push-action@ad44023a93711e3deb337508980b4b5e9bcdc5dc
        with:
          context: ./
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

```
This is responsible for creating and publishing the new docker image. 


### Workflow for CI/CD


## Naming conventions
This repository uses the snake-case naming convention

## File structure
### /relation_extraction 
The solution developed by group C to perform relation extraction on sentences with entity mentions and IRIs pointing to the entities.

### /concept_linking
Is the solution developed by group D to perform concept linking on sentences with entity mentions and IRIs pointing to the entities.

## Prerequisites
Run the command `pip install -r requirements.txt` to install the necessary libraries/modules for the solution.
Docker should be installed <a href="https://www.docker.com/products/docker-desktop/">download docker desktop</a>.

## Running the solution
### Run docker container using this command
`docker-compose up`

You can also do it manually:

`docker build -t server-image .`

`docker run --name server-container -p 8000:8000 server-image`

## Accessing the knox server
`ssh <your-aau-mail@student.aau.dk>@knox-preproc01.srv.aau.dk -L 8000:localhost:8000`

Note that the ports map to the ports used in the ssh command. 

## Server documentation

### post endpoints

#### /tripleconstruction
##### Summary:
The tripleconstruction expects JSON-formatted data and starts the process of concept_linking and relation_extraction in parallel.

##### Example query:
```json
[
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

```

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
|  200  | The post request was correctly formatted, and has been received by the server. | concept_linking and relation_extraction will be run in parallel.  |
|  422  | The post request was incorrectly formatted, and the server could therefore not parse the data. | Nothing is executed.  |
