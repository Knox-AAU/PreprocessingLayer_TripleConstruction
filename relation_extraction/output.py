import json
import requests

def format_output(output):
    formatted_output = {"triples": output}
    return formatted_output

def send_to_database_component(output):
    URL = "http://192.38.54.90/knowledge-base"
    response = requests.post(url=URL, json=format_output(output))
    