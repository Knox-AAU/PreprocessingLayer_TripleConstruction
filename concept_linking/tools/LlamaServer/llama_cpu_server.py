import os

import requests
from flask import Flask, request, jsonify
from llama_cpp import Llama
import time

model_filename = "llama-2-7b-chat.Q2_K.gguf"
model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf?download=true"
model_exp_size = 270000000

# Create a Flask object
app = Flask("Llama server")
model = None


@app.route('/llama', methods=['POST'])
def generate_response():
    start_time = time.time()
    global model

    try:
        data = request.get_json()
        # Check if the required fields are present in the JSON data
        if 'system_message' in data and 'user_message' in data and 'max_tokens' in data:
            system_message = data['system_message']
            user_message = data['user_message']
            max_tokens = int(data['max_tokens'])

            # Prompt creation
            prompt = f"""<s>[INST] <<SYS>>
            {system_message}
            <</SYS>>
            {user_message} [/INST]"""

            # Create the model if it was not previously created
            if model is None:
                # Put the location of to the GGUF model that you've download from HuggingFace here
                model_path = "./llama-2-7b-chat.Q2_K.gguf"

                # Create the model
                model = Llama(model_path=model_path, n_ctx=4092)

            # Run the model
            output = model(prompt, max_tokens=max_tokens, echo=True)
            end_time = time.time()
            elapsed_time = round((end_time - start_time), 2)
            print(f"Elapsed time: {elapsed_time} seconds")
            return jsonify(output)

        else:
            return jsonify({"error": "Missing required parameters"}), 400

    except Exception as e:
        return jsonify({"Error": str(e)}), 500


def download_model(model_filename, model_url):
    response = requests.get(model_url, stream=True)
    print("Downloading Llama model")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(model_filename, "wb") as model_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    model_file.write(chunk)

        # Check if the file exists after writing
        if os.path.exists(model_filename):
            print(f"Download successful: {model_filename}")
            return True
        else:
            print("Error: File not found after download.")
    else:
        print(f"Error: Failed to download file. Status code: {response.status_code}")

    return False


if __name__ == '__main__':
    # Use a while loop to repeatedly attempt to download the model
    while not (os.path.exists(model_filename) and os.path.getsize(model_filename) >= model_exp_size) and not download_model(
            model_filename, model_url):
        print("Retrying model download in 10 seconds...")
        time.sleep(10)

    # Once the model is available, start the Flask application
    if os.path.exists(model_filename) and os.path.getsize(model_filename) >= model_exp_size:
        print("Starting Flask application...")
        model_path = f"./{model_filename}"
        model = Llama(model_path=model_path, n_ctx=4092)
        app.run(host='0.0.0.0', port=5000, debug=True)
