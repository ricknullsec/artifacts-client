import requests
import json
import time


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
        self.update_Character(chracter_response_data)
        
    #This function returns the string representation of the character
    def __str__(self):
        return "Character " + self.name + " level " + str(self.level) + " with " + str(self.hp) + " hp and " + str(self.gold) + " gold."
    

    #This function updates the character with the new data
    def update_Character(self, chracter_response_data):
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
        print("Character " + self.name + " level " + str(self.level) +".")
        print("They are at location " + str(self.x) + ", " + str(self.y) + ".")
        print("They have " + str(self.hp) + "/" + str(self.max_hp) + " hp and " + str(self.gold) + " gold.")

    def timeout(self, cooldown):
        if cooldown > 0:
            print("You have to wait " + str(cooldown) + " seconds before you can take another action.")
            time.sleep(cooldown)

    #This function moves the character to the new location
    def move_Character(self, x, y):
        if self.x == x and self.y == y:
            print("You are already at that location.")
            return
        api_url = url + '/my/' + self.name + '/action/move'
        data = {'x': x, 'y': y}
        response = post_request(headers, api_url, data)
        self.timeout(response['data']['cooldown']['total_seconds'])
        self.update_Character(response['data']['character'])


    #This function makes the character fight
    def fight(self):
        api_url = url + '/my/' + self.name + '/action/fight'
        response = post_request(headers, api_url)
        for log in response['data']['fight']['logs']:
            print(log)
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['fight'])
        self.update_Character(response['data']['character'])
    

    #This function makes the character rest
    def rest(self):
        api_url = url + '/my/' + self.name + '/action/rest'
        response = post_request(headers, api_url)
        print("You are resting.")
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['rest'])
        self.update_Character(response['data']['character'])

    #This function makes the character gather
    def gather(self):
        api_url = f'{url}/my/{self.name}/action/gathering'
        response = post_request(headers, api_url)
        print(f"You gathered :{response['data']['details']['items']}")
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['gather'])
        self.update_Character(response['data']['character'])
    

    #this function makes the character unequip an item
    def unequip(self, slot, quantity = None):
        api_url = f'{url}/my/{self.name}/action/unequip'
        if quantity is None:
            data = {'slot': slot}
        else:
            data = {'slot': slot, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You unequipped {response['data']['item']['name']}")
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['unequip'])
        self.update_Character(response['data']['character'])

    #This function makes the character equip an item
    def equip(self, item_id, slot, quantity = None):
        api_url = f'{url}/my/{self.name}/action/equip'
        if quantity is None:
            data = {'code': item_id, 'slot': slot}
        else:
            data = {'code': item_id, 'slot': slot, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You equipped {response['data']['item']['name']} in slot {response['data']['slot']}")
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['equip'])
        self.update_Character(response['data']['character'])

    #This function crafts an item
    def craft(self, item_id, quantity = None):
        api_url = f'{url}/my/{self.name}/action/crafting'
        if quantity is None:
            data = {'code': item_id}
        else:
            data = {'code': item_id, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You crafted {response['data']['details']['items']}")
        self.timeout(response['data']['cooldown']['total_seconds'])
        #print(response['data']['craft'])
        self.update_Character(response['data']['character'])


    
  


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

def infinite_fight_loop():
    while True:
        if my_player.hp < (my_player.max_hp - 60):
            print("You are not at optimal health. You have " + str(my_player.hp) + "/" + str(my_player.max_hp) + " hp.")
            while my_player.hp < my_player.max_hp:
                my_player.rest()
        else:
            my_player.fight()






print(my_status())
my_player = load_character(CHARACTER_MAIN)

infinite_fight_loop()

#my_player.move_Character(0, 1)
#my_player.equip('wooden_staff', 'weapon')
#infinite_fight_loop()
#my_player.move_Character(2, 1)
#my_player.unequip('weapon')
#my_player.craft('wooden_staff')





