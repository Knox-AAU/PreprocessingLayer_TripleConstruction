# Use python as base image
FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY llama_cpu_server.py .
COPY requirements.txt .

#Install necessary build tools and dependencies for running C++(llama_cpp)
# This can be removed when app is in production and remote llama api server is reliable and used instead of local llama
# Install dependencies and curl
RUN apt-get update && apt-get install -y build-essential cmake curl && rm -rf /var/lib/apt/lists/*


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the model file from the URL if it doesn't exist
RUN test -e /app/llama-2-7b-chat.Q2_K.gguf || curl -o llama-2-7b-chat.Q2_K.gguf -LJO 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf?download=true'

# Expose port 5000 outside of the container
EXPOSE 5000

# Run llama_cpu_server.py when the container launches
CMD ["python", "-u", "-m", "llama_cpu_server", "--host", "0.0.0.0", "--port", "5000", "--reload"]
