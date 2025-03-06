import requests

#Function to make a get request to the API
def get_request(headers, api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
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