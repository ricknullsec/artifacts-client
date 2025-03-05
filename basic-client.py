import requests
import json


#Secret API key
#This is a secret key that is used to authenticate the user
#This key is stored in the art_secret.py file which is included in the gitignore file

from art_secret import API_KEY

url = 'https://api.artifactsmmo.com'
#data = {'key': 'value'}
headers = {'Content-Type': 'application/json'}

#Function to get the online status of the server
#Returns True if the server is online, False otherwise

def get_online_status():
    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json['data']['status'] == 'online'

#Gets the account status of the user and checks if the user is banned

def my_status():
    headers['Authorization'] = 'Bearer ' + API_KEY
    api_url = url + '/my/details'
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return "Error: " + response.text
    response_json = response.json()
    print(response)
    return "You are playing as " + response_json['data']['username'] + " and you are " + ("banned." if response_json['data']['banned'] else "not banned.")



print(get_online_status())
print(my_status())


