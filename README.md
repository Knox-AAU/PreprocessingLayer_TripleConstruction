# PreprocessingLayer_TripleConstruction

A repository for groups C (Relation Extraction) and D (Concept Linking) | KNOX 2023

PreprocessingLayer TripleConstruction is responsible for creating triples that can be utilised by group E to construct a knowledge graph.
The triples will be data stored in the form of a subject (entity IRI), predicate, and object (entity IRI), where the subject has some relation to the object.

## How to get started

### Helpful links:

1. <a href="https://github.com/Knox-AAU/PreprocessingLayer_TripleConstruction">Shared GitHub Repository for relation extraction and concept linking</a>.
2. <a href="https://www.overleaf.com/read/bqcxqfmhtvkx">The report on relation extraction.</a> Specifically read the abstract, and the following sections 'Requirements', 'Input and Output', 'Architecture for the multilingual RE solution utilising
   Llama', and 'Future works' section of the report. Key topics for relation extraction are: RDF, knowledge graphs, ontology, turtle, and data sets for relation extraction.
3. <a href="https://www.overleaf.com/4114212188xccnszjmqrdx#4089f4"> Overleaf document that is shared between all groups.</a> Specifically read the section regarding the KNOX pipeline and the section regarding pre-processing layer because this solution is very much reliant on groups A, B, D (minor reliance), and E.

## Prerequisites

If you wish to run the solution locally (not through docker). Run the command `pip install -r requirements.txt` to install the necessary libraries/modules for the solution.\
Docker should be installed if you want to run the solution in a container <a href="https://www.docker.com/products/docker-desktop/">download docker desktop here</a>.

## Running the solution

### Run docker container on local machine using this command

`docker-compose up --build`

### Deploy new version manually

Deployment is normally handled by watchtower on push to main. However, in case of the need of manual deployment, run

#### Access the knox server via ssh

`ssh <your-aau-mail@student.aau.dk>@knox-preproc01.srv.aau.dk -L <your_port>:localhost:4444`

Note that the ports map to the ports used in the ssh command give in "your port".

`sudo docker run -p 0.0.0.0:4444:<your_port> --add-host=host.docker.internal:host-gateway -e API_SECRET=*** -d ghcr.io/knox-aau/preprocessinglayer_tripleconstruction:main`

### Access through access API endpoint

`130.225.57.13/tripleconstruction-api/tripleconstruction`

### Direct access to endpoint

`192.38.54.87/tripleconstruction`

## Naming conventions

This repository uses the snake-case naming convention

## File structure

### /relation_extraction

The solution developed by group C to perform relation extraction on sentences with entity mentions and IRIs pointing to the entities.

### /concept_linking

Is the solution developed by group D to perform concept linking on sentences with entity mentions and IRIs pointing to the entities.

## Server documentation

### post endpoints

/tripleconstruction

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
        "entityMentions": [
          {
            "name": "Barrack Obama",
            "startIndex": 0,
            "endIndex": 12,
            "iri": "knox-kb01.srv.aau.dk/Barack_Obama"
          },
          {
            "name": "Michelle Obama",
            "startIndex": 27,
            "endIndex": 40,
            "iri": "knox-kb01.srv.aau.dk/Michele_Obama"
          }
        ]
      }
    ]
  }
]
```

##### Responses

| Code | Description                                                                                    | Schema                                                           |
| ---- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 200  | The post request was correctly formatted, and has been received by the server.                 | concept_linking and relation_extraction will be run in parallel. |
| 422  | The post request was incorrectly formatted, and the server could therefore not parse the data. | Nothing is executed.                                             |

## Configuration management

The solution utilises docker to fetch the latest updates that have been pushed to GitHub. This is done through GitHub worklfows.

### Workflow for testing and building project

The workflow for testing and building (Continuous integration) is defined as such.

```yml
name: test-and-build

on:
  push:
    branches: ["**"]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Setup python
        uses: actions/setup-python@v3
        with:
          python-version: 3.12.0

      - name: Install dependencies
        run: |
          echo "Installing dependencies"
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          echo "Testing..."
          python -m unittest || exit 1
        #Run all test

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Setup python
        uses: actions/setup-python@v3
        with:
          python-version: 3.12.0

      - name: Install dependencies
        run: |
          echo "Installing dependencies"
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build both projects if test pass
        run: |
          echo "Building projects"	          
          python3 relation_extraction/main.py     
          python3 concept_linking/main.py
```

This workflow runs the tests discovered in the /test directory. If those tests pass, then the solution will be built. The workflow run on a push to all branches in the repository.

### Workflow for building and deploying the docker image

Every time something is pushed to main a new docker image will be build and deployed(Continuous deployment).

```yml
name: build-and-deploy-docker-image

on:
  push:
    branches: ["main"]

env:
  # Use docker.io for Docker Hub if empty
  REGISTRY: ghcr.io
  # github.repository as <account>/<repo>
  IMAGE_NAME: ${{ github.repository }}

jobs:
  docker_build_and_deploy_image:
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

This workflow is responsible for creating and deploying the new docker image. The workflow runs only on push to the main branch.
