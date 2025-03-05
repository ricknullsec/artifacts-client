import requests
import json


from art_secret import API_KEY

url = 'https://api.artifactsmmo.com'
#data = {'key': 'value'}
headers = {'Content-Type': 'application/json'}

authtoken = 


def get_online_status():
    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json['data']['status'] == 'online'


def my_status():
    headers['Authorization'] = 'Bearer ' + API_KEY
    api_url = url + '/my/details'
    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    return "You are playing as " + response_json['data']['username'] + " and you are " + ("banned." if response_json['data']['banned'] else "not banned.")



print(get_online_status())
print(my_status())
