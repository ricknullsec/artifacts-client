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


class Character:
    def __init__(self, name, chracter_response_data):
        self.name = name
        self.level = chracter_response_data['level']
        self.xp = chracter_response_data['xp']
        self.max_xp = chracter_response_data['max_xp']
        self.gold = chracter_response_data['gold']
        
        #todo add skill levels

        self.hp = chracter_response_data['hp']
        self.max_hp = chracter_response_data['max_hp']

        #Add more stats here


        self.x = chracter_response_data['x']
        self.y = chracter_response_data['y']

        #todo add inventory and gear
        print("Character " + self.name + " level " + str(self.level) +" loaded.")


def get_request(headers, api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return "Error: " + response.text
    response_json = response.json()
    return response_json

def post_request(headers, api_url, data):
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
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

def load_character(character):
    api_url = url + '/characters/' + character
    character_class = Character(character, get_request(headers, api_url)['data'])
    
    return character_class
   
def get_map(x, y):
    api_url = url + '/maps/' + x + '/' + y
    return get_request(headers, api_url)

#Moves the character to a new location
def move_character(character, x, y):
    api_url = url + '/my/' + character + '/action/move'
    data = {'x': x, 'y': y}
    response = post_request(headers, api_url, data)




print(get_online_status())
print(my_status())
my_player = load_character(CHARACTER_MAIN)



#character_response_data = get_character_status()['data']
#print("You are playing as character " + character_response_data['name'] + " and you are leve " + str(character_response_data['level']) + ".")
#print("Your character is at location " + str(character_response_data['x']) + ", " + str(character_response_data['y']) + ".")
#current_map = get_map(str(character_response_data['x']), str(character_response_data['y']))
#print("Your current locations name is " + current_map['data']['name'] + " and it contains " + str(current_map['data']['content']) + ".")


#print(get_map('0', '1'))
#print(move_character(CHARACTER_MAIN, 0, 0))
