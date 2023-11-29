import requests

def format_output(output):
    formatted_output = {"triples": output}
    return formatted_output

def send_to_database_component(output):
    URL = "http://130.225.57.13/knox-api/triples"
    HEADERS = {"Access-Authorization":"internal_key"}
    PARAMS={"g": "http://knox_database"}
    response = requests.post(url=URL, json=format_output(output), params=PARAMS, headers=HEADERS)
    print(f"db component response: {response.text}")
    return response.text