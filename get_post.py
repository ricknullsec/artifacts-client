import requests
import time
import re

#Function to make a get request to the API
def get_request(headers, api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 499:
        error_message = response.get("error", {}).get("message", "")
        if "cooldown" in error_message:
            error_parse = re.search(r"(\d+\.?\d*) seconds left", error_message)
            if error_parse:
                print("Waiting on cooldown of {error_parse.group(1)}")
                time.sleep(float(error_parse.group(1)))
                response = requests.get(api_url, headers=headers)
    elif response.status_code != 200:
        raise Exception("Error: " + response.text)
    response_json = response.json()
    return response_json

#This function takes in the headers and the api_url
def post_request(headers, api_url, data = None):
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception("Error: " + response.text)
    response_json = response.json()
    return response_json