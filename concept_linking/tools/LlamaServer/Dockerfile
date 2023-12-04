# Before you create the docker image from this file, you must have either downloaded the llama-2-7b-chat.Q2_K.gguf file
# manually yourself, or run the server at least one time.

# Use python as base image
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./llama_cpu_server.py /app/llama_cpu_server.py
COPY ./llama-2-7b-chat.Q2_K.gguf /app/llama-2-7b-chat.Q2_K.gguf
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 outside of the container
EXPOSE 5000

# Run llama_cpu_server.py when the container launches
CMD ["python", "llama_cpu_server.py"]


#run to build image
#docker build -t llama-cpu-server .