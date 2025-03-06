import json
import time

from get_post import get_request, post_request
from class_Character import load_character

#Secret API key
#This is a secret key that is used to authenticate the user
#This key is stored in the art_secret.py file which is included in the gitignore file

from art_secret import API_KEY, CHARACTER_MAIN


url = 'https://api.artifactsmmo.com'
#data = {'key': 'value'}
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = 'Bearer ' + API_KEY


#Gets the online status of the game

def get_online_status():
    return get_request(headers, url)['data']['status'] == 'online'


#Gets the account status of the user and checks if the user is banned

def my_status():
    api_url = url + '/my/details'
    response_json = get_request(headers, api_url)
    return "You are playing as " + response_json['data']['username'] + " and you are " + ("banned." if response_json['data']['banned'] else "not banned.")


def get_map(x, y):
    api_url = url + '/maps/' + x + '/' + y
    return get_request(headers, api_url)


def infinite_fight_loop(x,y):
    my_player.move_Character(x,y)
    while True:
        if my_player.hp < (my_player.max_hp / 2):
            print("You are not at optimal health. You have " + str(my_player.hp) + "/" + str(my_player.max_hp) + " hp.")
            while my_player.hp < my_player.max_hp:
                my_player.rest()
        elif not my_player.check_inventory_full():
            my_player.deposit_all()
        else:
            my_player.move_Character(x,y)
            my_player.fight()


#loop for mining copper need to add checks for cooldown.
def infinit_mine_copper_loop():
    while True:
        if my_player.x != 2 and my_player.y != 0:
            my_player.move_Character(2,0)
        my_player.gather()
        if not my_player.check_inventory_full():
            my_player.deposit_all()





print(my_status())
my_player = load_character(CHARACTER_MAIN)



infinite_fight_loop(1,-2)





