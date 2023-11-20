# PreprocessingLayer_TripleConstruction

A repository for groups C (Relation Extraction) and D (Concept Linking) | KNOX 2023

## Run docker container using this command

`docker-compose up`

You can also do it manually:
`docker build -t server-image .`
`docker run --name server-container -p 8000:8000 server-image`

Use Postman to POST `exampleInput.json` to 0.0.0.0:8000/tripleconstruction

## Accessing the knox server

ssh <your-aau-mail@student.aau.dk>@knox-preproc01.srv.aau.dk -L 8000:localhost:8000
