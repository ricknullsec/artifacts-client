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
    api_url = f'{url}/maps/{str(x)}/{str(y)}'
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

def infinit_mine_iron_loop():
    while True:
        if my_player.x != 1 and my_player.y != 7:
            my_player.move_Character(1,7)
        my_player.gather()
        if not my_player.check_inventory_full():
            my_player.deposit_all()



def smelt_copper():
    while my_player.check_bank_item('copper_ore')['quantity'] > 0:
        my_player.move_Character(4,1)
        my_player.deposit_all()
        if my_player.check_bank_item('copper_ore')['quantity'] < my_player.inventory_max_items:
            my_player.withdraw_item('copper_ore', my_player.check_bank_item('copper_ore')['quantity'])
        else: 
            my_player.withdraw_item('copper_ore', my_player.inventory_max_items)
        my_player.move_Character(1,5)
        my_player.craft('copper', my_player.inventory[0]['quantity']/10)


print(my_status())
my_player = load_character(CHARACTER_MAIN[2])

infinit_mine_iron_loop()


#print(get_map(4,1))

#smelt_copper()
#infinit_mine_copper_loop()

#my_player.move_Character(2,1)
#my_player.craft('sticky_sword', 12)

#infinite_fight_loop(1,-2)





