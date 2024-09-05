from datetime import datetime
import json
import os
import shutil
import time

import requests

from utils import RiotAPI

played_games = []

def remove_old_game_play_data(recorded_video_path):
    if os.path.exists(recorded_video_path):
        # Iterate over all the files and directories in the specified path
        for filename in os.listdir(recorded_video_path):
            file_path = os.path.join(recorded_video_path, filename)
            try:
                # If it's a file, remove it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # If it's a directory, remove it and its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    
        
    recorded_video_path = "yt-temp"        
    if os.path.exists(recorded_video_path):
        # Iterate over all the files and directories in the specified path
        for filename in os.listdir(recorded_video_path):
            file_path = os.path.join(recorded_video_path, filename)
            try:
                # If it's a file, remove it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # If it's a directory, remove it and its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def init():
    # if not os.path.exists("media"):
    #     os.makedirs("media")

    if not os.path.exists("src"):
        os.makedirs("src")
        
    if not os.path.exists("yt"):
        os.makedirs("yt")
    if not os.path.exists("yt-temp"):
        os.makedirs("yt-temp")
    
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
            
def select_loser(position,players):
    for key,value in players.items():
        if position == value.split(":")[1]:
            return key.split(":")[0]
def get_player_team_index(game_name, tag_line, summoner_id):
    red_team = {}
    blue_team = {}
    red_count = 1
    blue_count = 1
    url =f"https://lol-web-api.op.gg/api/v1.0/internal/bypass/spectates/euw/{summoner_id}?hl=en_US"
    response = requests.get(url)
    # print(response.status_code)
    if response.status_code!= 200:
        return None, None, None, None
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
    if team == "Red":
        if position not in ["TOP","JUNGLE","MID","ADC","SUPPORT"]:
            try:
                loser = list(blue_team.keys())[int(index)-1].split(":")[0]
            except:
                loser = "out of range"
        else:
            loser = select_loser(position,blue_team)
    else:
        if position not in ["TOP","JUNGLE","MID","ADC","SUPPORT"]:
            try:
                loser = list(red_team.keys())[int(index)-1].split(":")[0]
            except:
                loser = "out of range"
        else:
            loser = select_loser(position,red_team)
    # print(loser)
    return team, index, loser, response.json()

def create_match_data(match_data, match_data_opgg , game_name, loser):
    lol_data ={}
    for player in match_data_opgg['data']['participants']:
        if game_name == player['summoner']['game_name']:
            player_data_opgg = player
            break
    # print("Loser:",loser)
    loser_player_data_opgg = {}
    for player in match_data_opgg['data']['participants']:
        if loser == player['summoner']['game_name']:
            loser_player_data_opgg = player
            break
    # if loser_player_data_opgg == {}:
    #     return {}
    champion_id = player_data_opgg['champion_id']
    spells = player_data_opgg['spells']
    try:
        loser_player_champion_id = loser_player_data_opgg['champion_id']
        lol_data['loser'] = match_data_opgg['data']['championsById'][str(loser_player_champion_id)]['name']
    except:
        lol_data['loser'] = "Not available"
    spell_1 = match_data_opgg['data']['spellsById'][str(spells[0])]['name']
    spell_2 = match_data_opgg['data']['spellsById'][str(spells[1])]['name']
    
    lol_data['mvp'] = {}
    lol_data['mvp']['champion'] = match_data_opgg['data']['championsById'][str(champion_id)]['name']
    lol_data['mvp']['rank'] = player_data_opgg['summoner']['league_stats'][0]['tier_info']['tier']
    lol_data['mvp']['spell'] = [spell_1,spell_2]
    
    lol_data['region'] = 'euw'
    lol_data['date'] = str(datetime.now().strftime("%d/%m/%Y"))
    lol_data['mvp']['name']  = game_name
    lol_data['patch'] ="14.17"

    return lol_data

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
        player_team, player_index,loser, match_data_opgg = get_player_team_index(game_name, tag_line, summoner_id)
        
        if player_team != None:
            thumbnail_data = create_match_data(match_data, match_data_opgg, game_name, loser)
        else:
            thumbnail_data = {}
        # if loser == "out of range":
        game_mode = match_data['gameMode']
        thumbnail_data['gamemode'] = game_mode
        return command, player_team, player_index, game_mode, thumbnail_data
    else:
        return None, None, None, None, None