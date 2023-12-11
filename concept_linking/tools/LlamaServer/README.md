# Tools: LlamaServer

## Description
Local API server based on Llama2.

## Getting started
It is possible to use the LlamaServer found in ../concept_linking/tools/LlamaServer
as a local llama api server.

The server uses a quantized version of the Llama2-7B model.
It needs to be present in the directory given above.
However, if it is not present just run the server a single time, and it will be downloaded.
This is necessary before trying to create a docker image for the server.

[//]: # (This instance has been optimized for usage with Nvidia CUDA supported GPUs'.)

[//]: # (The software will automatically detect a valid CUDA gpu if one is present.)

[//]: # (If not, the solution will fall back to using the CPU.)

## Requirements
Install the requirements for this solution

Navigate to the following directory

```
../concept_linking/tools/LlamaServer/
```

And run the following command
```
pip install -r requirements.txt
```

Since this is meant as a tool for running Llama locally on Windows. It is required to have a C++ installation.
C++ can be installed via the Visual Studio Installer.
Select "Desktop development with C++"

## Docker
To build the server as a docker image, change the directory in a terminal to ../concept_linking/tools/LlamaServer.
Run the following command

```
docker build -t llama-cpu-server . 
```

* Open Docker desktop
* Select Images, under 'Actions' select 'run'
* A prompt will now appear, expand the 'Optional settings'
* Under 'Ports' set 'Host Port' to 5000
* Press run.

The server should now be up and running
