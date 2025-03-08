import requests
import time
import re

#Function to make a get request to the API
def get_request(headers, api_url):
    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    if response.status_code == 499:
        error_message = response_json['error']['message']
        if "cooldown" in error_message:
            error_parse = re.search(r"(\d+\.?\d*) seconds left", error_message)
            if error_parse:
                print("Waiting on cooldown of {error_parse.group(1)}")
                time.sleep(float(error_parse.group(1)))
                return get_request(headers, api_url)
    elif response.status_code != 200:
        raise Exception("Error: " + response.text)
    else:
        return response_json

#This function takes in the headers and the api_url
def post_request(headers, api_url, data = None):
    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    if response.status_code == 499:
        error_message = response_json['error']['message']
        if "cooldown" in error_message:
            error_parse = re.search(r"(\d+\.?\d*) seconds left", error_message)
            if error_parse:
                error_time = error_parse.group(1)
                print(f"Waiting on cooldown of {error_time}")
                time.sleep(float(error_parse.group(1)))
                return post_request(headers, api_url, data)
    elif response.status_code != 200:
        raise Exception("Error: " + response.text)
    else:
        return response_json