import json
import multiprocessing

import time
from utils import Tools
import logging

from utils import game_controller, YoutubeHandler
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="A script that processes some input")

# Add arguments
parser.add_argument("-y", "--yt", type=bool, help="to ty enable --yt True")
args = parser.parse_args()
enable_yt = args.yt
# if enable_yt:
#     print("Youtube automation is enabled")
# else:
#     print("Youtube automation is disabled")
# exit()
logging.basicConfig(filename='../LoL stream.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

api_key = "RGAPI-e402533c-0411-4121-ab3a-62001784ae2f"
youtube_record_path = r"C:\Users\zandt\Desktop\Gameplay"
Tools.init()

uploader_process_running = multiprocessing.Value('b', False)
uploader_lock = multiprocessing.Lock()

def run_video_uploader():
    YoutubeHandler.youtube_runner()

played_games = []
def Run(game_run_command, player_team, player_index, game_mode,thumbnail_data):
    
    with open("yt-temp/match_data.json", 'w') as json_file:
        json.dump(thumbnail_data, json_file)

    print(f"   [-] player team: {player_team}")
    print(f"   [-] player index: {player_index}")
    
    gameController = game_controller.ControlGamePlay(player_team, player_index, game_run_command)
    out = gameController.control(game_mode)
    if out == "crashed":
        played_games.pop()
    elif enable_yt:
        YoutubeHandler.move_all_files(youtube_record_path)
        with uploader_lock:
            if not uploader_process_running.value:
                uploader_process_running.value = True
                uploader_process = multiprocessing.Process(target=uploader_worker)
                uploader_process.start()

def uploader_worker():
    run_video_uploader()
    with uploader_lock:
        uploader_process_running.value = False

if __name__ == "__main__":
    Tools.player_config(api_key)
    
    print("========> Debug 1: Initial test. <===========")
    count = 0
    with open("src/player_list.txt", "r") as file:
    # with open("../playerLinks.txt", "r") as file:
        player_all = file.readlines()
    
    if len(player_all) == 0:
        print("Add player in player.txt (Format: game name:tag line:summoner id)")
        exit()
    while True:
        game_name, tag_line, summoner_id,player_puuid = player_all[count % len(player_all)].strip().split(":")
        print("[+] Player: " + game_name)
        count += 1
        if (count == len(player_all)):
            count = 0
        try:
            # print(playerLink)
            game_run_command, player_team, player_index, game_mode,thumbnail_data = Tools.get_game_run_command(game_name, tag_line, summoner_id,player_puuid, api_key)
            if game_run_command in played_games:
                print("   [-] Already played game found")
                time.sleep(1)
                continue
            elif game_run_command == None:
                print("   [-] Live game not found (Riot API)")
                time.sleep(1)
                continue
            elif player_team == None:
                print("   [-] Live game not found (OP.gg API)")
                time.sleep(1)
                continue
            else:
                played_games.append(game_run_command)
                Tools.remove_old_game_play_data(youtube_record_path)
                Run(game_run_command,player_team, player_index, game_mode,thumbnail_data)
                

        except Exception as e:
            count -= 1
            print("Error:", str(e))
            logging.error("Main(__name__) Error:", str(e))
            break