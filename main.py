print("You're using Ecto's Dungeon Generator version 0.1.0 Alpha! Please support me by subscribing to my YouTube channel @EctoPhasic and @PhasiCat!")

import json
import time
import random

# Initialize Dungeon variables and lists
editormode = False
debug = False
dungeon = []
editingRoom = {}
items = []
enemies = []
itemdata = {}
enemydata = {}

# Initialize Player
inventory = {}
life = 95
maxlife = 100
action = ""
currentRoom = 0

# Function to create an enemy
def createEnemy(mindamage, maxdamage, hp, name):
    enemydata = {"name": name, "mindamage": mindamage, "maxdamage": maxdamage, "hp": hp}
    enemies.append(enemydata)

# Function to create an item
def createItem(damage, idnum, name):
    itemdata = {"damage": damage, "idnum": idnum, "name": name}
    items.append(itemdata)

# Function to create a room
def createRoom(desc, item, doors, enemy):  # doors should be a list of room ids
    editingRoom = {"desc": desc, "item": item, "doors": doors, "enemies": enemy}
    dungeon.append(editingRoom)

# Function to save dungeon to a JSON file
def createDungeon():
    data = {
        "dungeon": dungeon,
        "items": items,
        "enemies": enemies
    }
    with open('name.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Level saved")

def decideAction(action):
    global currentRoom, life, inventory

    room = dungeon[currentRoom]

    if action == "1":  # Get Item
        if room["item"]:
            item = room["item"]
            inventory[item["idnum"]] = item
            print(f"You picked up {item['name']}.")
        else:
            print("No items in this room.")
    
    elif action == "2":  # Fight
        if room["enemies"]:
            for enemy in room["enemies"]:
                print(f"Fighting {enemy['name']} (HP: {enemy['hp']}, Damage: {enemy['mindamage']}-{enemy['maxdamage']})")
                enemy_hp = enemy['hp']
                while enemy_hp > 0 and life > 0:
                    damage = random.randint(4, 6)  # Assuming player damage for simplicity
                    enemy_hp -= damage
                    print(f"You hit the {enemy['name']} for {damage} damage!")
                    if enemy_hp <= 0:
                        print(f"You defeated the {enemy['name']}!")
                        break
                    enemy_damage = random.randint(enemy['mindamage'], enemy['maxdamage'])
                    life -= enemy_damage
                    print(f"The {enemy['name']} hits you for {enemy_damage} damage!")
                    if life <= 0:
                        print("You have been defeated! Game over!")
                        exit()
            # After fight, heal player
            life = min(life + 10, maxlife)
            print(f"Health restored! Current health: {life}/{maxlife}")
        else:
            print("No enemies in this room to fight.")
    
    elif action == "3":  # Enter Door
        if room["doors"]:
            next_room = random.choice(room["doors"])  # Choose a random door
            print(f"You enter room {next_room}.")
            currentRoom = next_room
        else:
            print("There are no doors in this room.")
    
    elif action == "4":  # Equip Item
        if inventory:
            print("Your Inventory:")
            for item in inventory.values():
                print(f"{item['name']} (Damage: {item['damage']})")
            equip_item = input("Enter item name to equip: ")
            # Equip the item (just a placeholder here, could have effects)
            print(f"You equipped {equip_item}.")
        else:
            print("No items in your inventory.")
    
    elif action == "5":  # Check Health
        print(f"Your health: {life}/{maxlife}")
    
    elif action == "6":  # View Inventory
        if inventory:
            print("Your Inventory:")
            for item in inventory.values():
                print(f"{item['name']} (Damage: {item['damage']})")
        else:
            print("Your inventory is empty.")

# Function to describe the room
def describeRoom():
    room = dungeon[currentRoom]
    print(f"Room {currentRoom}: {room['desc']}")
    
    if room["item"]:
        print(f"Item in this room: {room['item']['name']}")
    else:
        print("No items in this room.")
    
    if room["enemies"]:
        print("Enemies in this room:")
        for enemy in room["enemies"]:
            print(f"- {enemy['name']} (HP: {enemy['hp']}, Damage: {enemy['mindamage']}-{enemy['maxdamage']})")
    
    print(f"Health: {life}/{maxlife}")
    print("Actions: 1: Get Item | 2: Fight | 3: Enter Door | 4: Equip Item | 5: Check Health | 6: View Inventory")
    action = input("What do you want to do? (1, 2, 3, 4, 5, or 6): ")
    return action

# If in editor mode, create dungeon and save
if editormode:
    createDungeon()
    print("Dungeon file generated! Closing in 5 seconds...")
    time.sleep(5)
    exit()

# Load the data back from JSON file
print("Loading dungeon")
with open('example.json', 'r') as file:
    data = json.load(file)

print("Loaded! Extracting data...")
# Extract individual objects
dungeon = data["dungeon"]
items = data["items"]
enemies = data["enemies"]

print("Done! Finishing up...")
if debug:
    print("Dungeon:", dungeon)
    print("Items:", items)
    print("Enemies:", enemies)

# Main game loop
while True:
    action = describeRoom()
    decideAction(action)
