import json
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Monters.data_monters import monters
from module.data_game.Player.level import level
import asyncio
def save_inventory_data(player_inventory):
    with open('data/player_inventory.json', 'w') as file:
        json.dump(player_inventory, file)
def save_player_data(data=None):
    if data is None:
        data = player
    serializable_player = {}
    for user_id, pdata in data.items():
        serializable_data = pdata.copy()
        if isinstance(serializable_data.get('money'), SharedMoney):
            serializable_data['money'] = serializable_data['money'].to_dict()
        serializable_player[user_id] = serializable_data

    with open('data/player_data.json', 'w') as f:
        json.dump(serializable_player, f, indent=4)

def load_inventory_data():
    global player_inventory
    try:
        with open('data/player_inventory.json', 'r') as file:
            player_inventory = json.load(file)
    except FileNotFoundError:
        player_inventory = {}
    return player_inventory


def load_player_data():
    global player
    try:
        with open('data/player_data.json', 'r') as f:
            data = json.load(f)
            for user_id, p_data in data.items():
                if isinstance(p_data.get('money'), dict):
                    p_data['money'] = SharedMoney.from_dict(p_data['money'])
            player = data
    except FileNotFoundError:
        player = {}
    return player


