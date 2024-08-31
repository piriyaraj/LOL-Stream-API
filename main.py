import subprocess
import datetime
import psutil
import time
from utils import RiotAPI, Tools
import logging
import os
import pygetwindow as gw
from utils import game_controller

logging.basicConfig(filename='../LoL stream.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

api_key = "RGAPI-e402533c-0411-4121-ab3a-62001784ae2f"

Tools.init()

restartFlag = False
played_games = []
def Run(game_run_command, player_team, player_index):
    global  restartFlag
    
    # playerTeam = None

    # base_directory = os.path.abspath('yt')
    # current_datetime = datetime.datetime.now()
    # folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    # new_folder_path = os.path.join(base_directory, folder_name)
    # os.makedirs(new_folder_path, exist_ok=True)
    # start_time = time.time()
    # playerTeam, playerIndex, driver, no_of_played_game, spectate_button = get_commands(
    #     playerLink, playerName, new_folder_path, driver, playerTeam, playerIndex, no_of_played_game)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("  -Time took:(sec)", execution_time)
    # logging.info(f"  -Time took:(sec) {execution_time}")
    # playerTeam, playerIndex, driver, no_of_played_game = "Red",1,driver, 3
    # if playerTeam != "None" and playerTeam != "Not found":
    #     if not (restartFlag):
    #         delayTime = 150 - int(execution_time)
    #         # print("  -New game start delay:(sec)",delayTime)

    #         # if delayTime > 0:
    #         #     logging.info(f"  -New game start delay:(sec): {delayTime}")
    #             # time.sleep(delayTime)
    #     else:
    #         restartFlag = False
    #     start_time = time.time()
    # print("   -",game_run_command)
    print(f"   [-] player team: {player_team}")
    print(f"   [-] player index: {player_index}")
    # subprocess.run(game_run_command, shell=True)
    gameController = game_controller.ControlGamePlay(player_team, player_index, game_run_command)
    out = gameController.control()
    if out == "crashed":
        played_games.pop()
    #     end_time = time.time()
    #     print("  -Game played time:(sec)", end_time-start_time)
    #     logging.info(f"  -Game played time:(sec): {end_time-start_time}")
    #     if out == "crashed":
    #         logging.info(f"  -Game crashed")
    #         print(f"  -Game crashed")
    #         removeFolder(new_folder_path)
    #         changePlayedGame()
    #         logging.info(f"  -Removed game id from played list")
    #         restartFlag = True
    #     else:
    #         logging.info(f"  -Start YT upload")
    #         uploader_process = multiprocessing.Process(
    #             target=run_video_uploader, args=(new_folder_path,))
    #         uploader_process.start()

    # elif playerTeam == "Not found":
    #     removeFolder(new_folder_path)
    #     restartFlag = False
    # else:
    #     removeFolder(new_folder_path)
    #     restartFlag = False
    #     driver = None
    #     closeGame()
    #     pass



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
            game_run_command, player_team, player_index = Tools.get_game_run_command(game_name, tag_line, summoner_id,player_puuid, api_key)
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
                # print("   [-] Time delay: 150 seconds")
                # time.sleep(150)
                Run(game_run_command,player_team, player_index)
                

        except Exception as e:
            count -= 1
            print("Error:", str(e))
            logging.error("Main(__name__) Error:", str(e))
            break