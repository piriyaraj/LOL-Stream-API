import os
import time

import requests

from utils import RiotAPI

played_games = []

def init():
    if not os.path.exists("media"):
        os.makedirs("media")

    if not os.path.exists("src"):
        os.makedirs("src")
    
def player_config(api_key):
    if not os.path.exists("src/player_list.txt"):
        # If the file doesn't exist, create it
        open("src/player_list.txt", "w").close()
    
    if not os.path.exists("../player.txt"):
        open("../player.txt", "w").close()
    # Read the contents of player.txt
    with open("../player.txt", "r") as file:
        player_all = file.readlines()

    # Create a set for the players in player.txt for easy lookup
    current_players = set([player.strip() for player in player_all])

    # Read the current src/player_list.txt contents
    with open("src/player_list.txt", "r") as file:
        existing_players = file.readlines()

    # Create a dictionary from the existing src/player_list.txt contents
    existing_dict = {}
    for player in existing_players:
        game_name, tag_line,summoner_id, puuid = player.strip().split(":")
        existing_dict[f"{game_name}:{tag_line}:{summoner_id}"] = puuid

    # Create a list to store the updated content
    updated_list = []

    # Process each player in player.txt
    for player in current_players:
        game_name, tag_line, summoner_id = player.split(":")
        player_key = f"{game_name}:{tag_line}:{summoner_id}"

        # Check if the player already exists in src/player_list.txt
        if player_key in existing_dict:
            # If it exists, add it to the updated list with the existing puuid
            updated_list.append(f"{player_key}:{existing_dict[player_key]}")
        else:
            # If it doesn't exist, find the puuid and add it to the updated list
            status, puuid = RiotAPI.get_puuid(game_name, tag_line, api_key)
            if status:
                updated_list.append(f"{player_key}:{puuid}")
            time.sleep(5)
    # Write the updated list back to src/player_list.txt
    with open("src/player_list.txt", "w") as file:
        for player in updated_list:
            file.write(player + "\n")
            
def get_player_team_index(game_name, tag_line, summoner_id):
    red_team = {}
    blue_team = {}
    red_count = 1
    blue_count = 1
    url =f"https://lol-web-api.op.gg/api/v1.0/internal/bypass/spectates/euw/{summoner_id}"
    response = requests.get(url)
    # print(response.status_code)
    if response.status_code!= 200:
        return None, None
    for players in response.json()['data']['participants']:
        if players['team_key'] == "RED":
            red_team[f"{players['summoner']['game_name']}:{players['summoner']['tagline']}"] = f"{red_count}:{players['position']}"
            red_count +=1
        else:
            blue_team[f"{players['summoner']['game_name']}:{players['summoner']['tagline']}"] = f"{red_count}:{players['position']}"
            blue_count +=1
    try:
        index, position = red_team[f"{game_name}:{tag_line}"].split(":")
        team ="Red"
    except:
        index, position = blue_team[f"{game_name}:{tag_line}"].split(":")
        team = "Blue"
    # print("red_team:", red_team)
    # print("blue_team:", blue_team)

    if position == "TOP":
        index = 1
    elif position == "JUNGLE":
        index = 2
    elif position == "MID":
        index = 3
    elif position == "ADC":
        index = 4
    elif position == "SUPPORT":
        index = 5
    return team, index

def get_game_run_command(game_name, tag_line, summoner_id,player_puuid,api_key):
    status, match_data = RiotAPI.get_in_game_match_data(player_puuid, api_key)
    if status:
        observer_decrypt_key = match_data['observers']['encryptionKey']
        game_mode = match_data['gameMode']
        game_id = match_data['gameId']
        command = f"""cd /d "C:\Riot Games\League of Legends\Game" & "League of Legends.exe" "spectator spectator.euw1.lol.pvp.net:8080 {observer_decrypt_key} {game_id} EUW1" "-UseRads" """
        # if command in played_games:
        #     return "Already played game", None, None
        # else:
        #     played_games.append(command)
        player_team, player_index = get_player_team_index(game_name, tag_line, summoner_id)
        return command, player_team, player_index, game_mode
    else:
        return None, None, None, None