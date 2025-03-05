import requests
import json


#Secret API key
#This is a secret key that is used to authenticate the user
#This key is stored in the art_secret.py file which is included in the gitignore file

from art_secret import API_KEY, CHARACTER_MAIN

url = 'https://api.artifactsmmo.com'
#data = {'key': 'value'}
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = 'Bearer ' + API_KEY

#Function to make a get request to the API
#This function takes in the headers and the api_url

def get_request(headers, api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return "Error: " + response.text
    response_json = response.json()
    return response_json

#Gets the online status of the game

def get_online_status():
    return get_request(headers, url)['data']['status'] == 'online'


#Gets the account status of the user and checks if the user is banned

def my_status():
    api_url = url + '/my/details'
    response_json = get_request(headers, api_url)
    return "You are playing as " + response_json['data']['username'] + " and you are " + ("banned." if response_json['data']['banned'] else "not banned.")

def get_character_status():
    api_url = url + '/characters/' + CHARACTER_MAIN
    return get_request(headers, api_url)
   
def get_map(x, y):
    api_url = url + '/maps/' + x + '/' + y
    return get_request(headers, api_url)

#Moves the character to a new location
def move_character(character, x, y):
    pass


print(get_online_status())
print(my_status())

character_response_data = get_character_status()['data']
print("You are playing as character " + character_response_data['name'] + " and you are leve " + str(character_response_data['level']) + ".")
print("Your character is at location " + str(character_response_data['x']) + ", " + str(character_response_data['y']) + ".")
current_map = get_map(str(character_response_data['x']), str(character_response_data['y']))
print("Your current locations name is " + current_map['data']['name'] + " and it contains " + str(current_map['data']['content']) + ".")


print(get_map('0', '1'))