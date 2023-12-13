# Use python as base image
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY llama_cpu_server.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Check if the model file exists, and if not, download it using the provided function
RUN python -c "from llama_cpu_server import download_model; download_model('llama-2-7b-chat.Q2_K.gguf', 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf?download=true')"


# Expose port 5000 outside of the container
EXPOSE 5000

# Run llama_cpu_server.py when the container launches
CMD ["python", "llama_cpu_server.py"]
