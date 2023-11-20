import requests
import urllib.parse

def POST_corenlp(sentences):
    url = "https://corenlp.run/?properties=%7B%22annotators%22%3A%20%22tokenize%2Cssplit%2Copenie%22%2C%20%22date%22%3A%20%222023-10-26T15%3A50%3A03%22%7D&pipelineLanguage=en"

    payload = "".join([" " + s for s in sentences]) #join array of sentences to one long string.
    headers = {
    'authority': 'corenlp.run',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://corenlp.run',
    'referer': 'https://corenlp.run/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
