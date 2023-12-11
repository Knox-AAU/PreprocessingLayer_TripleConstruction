from flask import Flask, request, jsonify
import json
import os
from relation_extraction.relation_extractor import RelationExtractor

app = Flask(__name__)

@app.route('/tripleconstruction', methods=["POST"])
def do_triple_construction():
    print("Received POST request...")

    authorization_header = request.headers.get("Authorization")

    if authorization_header != os.getenv("API_SECRET"):
        message = "Unauthorized"
        return jsonify(error=f"Error occurred! {message}"), 401
    
    try:
        post_data = request.get_data().decode('utf-8')
        post_json = json.loads(post_data)

        RelationExtractor.begin_extraction(post_json)
        #Begin ConceptLinking

        message = "Post request was successfully processed. Relation extraction and concept linking completed."
        return jsonify(message=message), 200

    except Exception as e:
        return jsonify(error=f"Error occured: {str(e)}"), 422

@app.errorhandler(404)
def page_not_found(error):
    message = "Invalid endpoint"
    return jsonify(error=message), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)