from get_post import post_request, get_request
import time
from art_secret import API_KEY
from datetime import datetime, timezone
url = 'https://api.artifactsmmo.com'
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = 'Bearer ' + API_KEY




#Loads the character from the API
def load_character(character):
    api_url = url + '/characters/' + character
    character_class = Character(character, get_request(headers, api_url)['data'])
    return character_class
   
   
#This class represents a character in the game


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
        self.cooldown_exp = chracter_response_data['cooldown_expiration']
        
        #todo add skill levels
        self.gearcrafting_level = chracter_response_data['gearcrafting_level']

        
        self.hp = chracter_response_data['hp']
        self.max_hp = chracter_response_data['max_hp']
        self.cooldown = chracter_response_data['cooldown']

        #Add more stats here


        self.x = chracter_response_data['x']
        self.y = chracter_response_data['y']

        #todo add inventory and gear
        self.inventory_max_items = chracter_response_data['inventory_max_items']
        self.inventory = chracter_response_data['inventory']
        print("Character " + self.name + " level " + str(self.level) +".")
        print("They are at location " + str(self.x) + ", " + str(self.y) + ".")
        print("They have " + str(self.hp) + "/" + str(self.max_hp) + " hp and " + str(self.gold) + " gold.")


    def wait_for_cooldown(self):
        expiration_time = datetime.strptime(self.cooldown_exp, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        wait_time = (expiration_time - current_time).total_seconds()
        print(f"Expiration time: {expiration_time}")
        print(f"Current time: {current_time}")
        start = time.monotonic()  # Track time more accurately
        if wait_time > 0:
            print("You have to wait " + str(wait_time) + " seconds before you can take another action.")
            time.sleep(wait_time)
            end = time.monotonic()
            actual_sleep = end - start
            print(f"Slept for: {actual_sleep:.2f} seconds")

    def timeout(self, cooldown):
        if cooldown > 0:
            print("You have to wait " + str(cooldown) + " seconds before you can take another action.")
            start = time.monotonic()  # Track time more accurately
            time.sleep(cooldown)
            end = time.monotonic()
            actual_sleep = end - start
            print(f"Slept for: {actual_sleep:.2f} seconds")


    #This function moves the character to the new location
    def move_Character(self, x, y):
        if self.x == x and self.y == y:
            print("You are already at that location.")
            return
        api_url = url + '/my/' + self.name + '/action/move'
        data = {'x': x, 'y': y}
        response = post_request(headers, api_url, data)
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    #This function makes the character fight
    def fight(self):
        api_url = url + '/my/' + self.name + '/action/fight'
        response = post_request(headers, api_url)
        for log in response['data']['fight']['logs']:
            print(log)
        #print(response['data']['fight'])
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])
    

    #This function makes the character rest
    def rest(self):
        api_url = url + '/my/' + self.name + '/action/rest'
        response = post_request(headers, api_url)
        print("You are resting.")
        #print(response['data']['rest'])
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    #This function makes the character gather
    def gather(self):
        api_url = f'{url}/my/{self.name}/action/gathering'
        response = post_request(headers, api_url)
        print(f"You gathered :{response['data']['details']['items']}")
        #print(response['data']['gather'])
        self.update_Character(response['data']['character'])
        print(response['data']['cooldown']['remaining_seconds'])
        print(response['data']['cooldown']['total_seconds'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])
    

    #this function makes the character unequip an item
    def unequip(self, slot, quantity = None):
        api_url = f'{url}/my/{self.name}/action/unequip'
        if quantity is None:
            data = {'slot': slot}
        else:
            data = {'slot': slot, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You unequipped {response['data']['item']['name']}")
        #print(response['data']['unequip'])
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    #This function makes the character equip an item
    def equip(self, item_id, slot, quantity = None):
        api_url = f'{url}/my/{self.name}/action/equip'
        if quantity is None:
            data = {'code': item_id, 'slot': slot}
        else:
            data = {'code': item_id, 'slot': slot, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You equipped {response['data']['item']['name']} in slot {response['data']['slot']}")
        #print(response['data']['equip'])
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    #This function crafts an item
    def craft(self, item_id, quantity = None):
        api_url = f'{url}/my/{self.name}/action/crafting'
        if quantity is None:
            data = {'code': item_id}
        else:
            data = {'code': item_id, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        print(f"You crafted {response['data']['details']['items']}")
        #print(response['data']['craft'])
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    def print_inventory(self):
        print("You have the following items in your inventory:")
        inventory_size = 0
        for item in self.inventory:
            while item['quantity'] > 0:
                print(f"{item['code']} x {item['quantity']}")
                inventory_size += item['quantity']
                break
        print(f'You have {inventory_size}/{self.inventory_max_items} items in your inventory.')


    def check_inventory_full(self):
        inventory_size = 0
        for item in self.inventory:
            while item['quantity'] > 0:
                inventory_size += item['quantity']
                break
        return inventory_size < (self.inventory_max_items - 1)
    

    #This function deposits items into the bank
    def deposit_item(self, item_id, quantity = 1):
        api_url = f'{url}/my/{self.name}/action/bank/deposit'
        data = {'code': item_id, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])


    #This function withdraws items from the bank
    def withdraw_item(self, item_id, quantity = 1):
        api_url = f'{url}/my/{self.name}/action/bank/withdraw'
        data = {'code': item_id, 'quantity': quantity}
        response = post_request(headers, api_url, data)
        self.update_Character(response['data']['character'])
        self.timeout(response['data']['cooldown']['remaining_seconds'])

    def deposit_all(self):
        self.move_Character(4,1)
        for item in self.inventory:
            if item['quantity'] > 0 and item['code'] != '':
                self.deposit_item(item['code'], item['quantity'])


    def get_my_bank_items(self):
        api_url = f'{url}/my/bank/items'
        response = get_request(headers, api_url)
        return response['data']
    


    def check_bank_item(self, item_id):
        bank_items = self.get_my_bank_items()
        for item in bank_items:
            if item['code'] == item_id:
                return item
        return None
                

