import logging
import os
from time import sleep
import subprocess
import time
import psutil
import pyautogui
import pydirectinput
from PIL import ImageGrab
from PIL import Image

import time
import pygetwindow as gw


def closeGame():
    target_window_title = "league of legends (TM) client"
    download_failed = "Download Failed"
    system_failed = "System Error"

    # Get a list of all open windows
    open_windows = gw.getWindowsWithTitle(target_window_title)
    download_failed_window = gw.getWindowsWithTitle(download_failed)

    if download_failed_window:
        while True:
            # print(f"{download_failed} is open.")
            # Close the window

            download_failed_window = gw.getWindowsWithTitle(download_failed)
            if download_failed_window:
                download_failed_window[0].close()
                # print(f"{download_failed} has been closed.")
                time.sleep(5)
                continue
            else:
                break
    # else:
    #     print(f"{download_failed} is not open.")
        
    if open_windows:
        while True:
            # print(f"{target_window_title} is open.")
            # Close the window

            open_windows = gw.getWindowsWithTitle(target_window_title)
            if open_windows:
                open_windows[0].close()
                # print(f"{target_window_title} has been closed.")
                time.sleep(5)
                continue
            else:
                break
    # else:
    #     print(f"{target_window_title} is not open.")


    system_failed_windows = gw.getWindowsWithTitle(system_failed)
    if system_failed_windows:
        while True:
            print(f"{system_failed} is open.")
            # Close the window

            system_failed_windows = gw.getWindowsWithTitle(system_failed)
            if system_failed_windows:
                system_failed_windows[0].close()
                time.sleep(3)
                print(f"{system_failed} has been closed.")
                time.sleep(5)
                continue
            else:
                break
    # else:
    #     print(f"{system_failed} is not open.")
class ControlGamePlay:
    def __init__(self, playerTeam, playerIndex, game_run_command) -> None:
        # self.__replay_file_dir = os.path.abspath(r'.\media\gameplay')
        self.__player_team = playerTeam
        self.__player_index = str(playerIndex)
        self.game_run_command = game_run_command

    def control(self, game_mode):
        self.close_game_setup()
        print("   [-] Start game control")
        subprocess.Popen( self.game_run_command, shell=True)

        print("      [*] Game mode:",game_mode)
        status = self.start_game()
        if status == False:
            print("      [-] Game failed to open")
            closeGame()
            return "crashed"

        time.sleep(5)
        # print("   -click center of the screen")
        # Get the size of the screen
        screen_width, screen_height = pydirectinput.size()

        # Calculate the center of the screen
        center_x = int(screen_width / 2)
        center_y = int(screen_height / 2)

        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        pydirectinput.keyDown('n')
        pydirectinput.keyUp('n')
        sleep(1)
        pydirectinput.keyDown('u')
        pydirectinput.keyUp('u')
        sleep(2)
        
        if game_mode == "CLASSIC":
            # scoreboard
            pydirectinput.keyDown('o')
            pydirectinput.keyUp('o')
            sleep(1)
            # timeline hide
            
            # print_progress(56, self.total, prefix='Gameplay recording:')
            # select champion
        
            print("      [*] Selecting player")
            self.__select_player()

            sleep(2)
            # Extend character stats
            pydirectinput.keyDown('c')
            pydirectinput.keyUp('c')
            sleep(1)
        # print_progress(59, self.total, prefix='Gameplay recording:')
        # zoom out
        print("      [*] Zoom out the screen!")
        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        # Press and hold Ctrl+Shift+Z
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('z')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyUp('shift')
        pydirectinput.keyUp('z')
        # Move mouse pointer down 5 times
        pyautogui.scroll(-700)

        self.close_game()
        # sleep(60*3)
        return True

    def start_game(self):
        print('      [*] Wait for open game')
        
        # Check if the image file exists
        image_path = os.path.abspath("src\img\startButton.png")

        if not os.path.exists(image_path):
            print("      [*] Image not found:", image_path)
            return False
        
        target_image = Image.open(image_path)
        count = 0
        while True:
            screenshot = pyautogui.screenshot()  # Take a screenshot of the entire screen
            
            # Try locating the target image with a lower confidence level
            try:
                result = pyautogui.locateOnScreen(target_image, confidence=0.5)
            except pyautogui.ImageNotFoundException as e:
                # print(f"  -Image not found: {e}")
                result = None

            if result is not None:
                button_position = pyautogui.center(result)
                print("      [*] Game started")
                return True  # Return True after clicking
            else:
                time.sleep(10)  # Wait for 10 seconds before checking again
                if count >= 2 * 60:
                    return False
                count += 10

    def close_game(self):
        print('      [*] Wait for closing game')
        
        # Load the target image
        image_path = os.path.abspath("src/img/closeButton.png")
        if not os.path.exists(image_path):
            print("      [*] Close button image not found:", image_path)
            return False
        
        target_image = Image.open(image_path)

        while True:
            try:
                # Attempt to locate the close button on the screen
                result = pyautogui.locateOnScreen(target_image, confidence=0.80)
            except pyautogui.ImageNotFoundException as e:
                # print(f"  -Image not found: {e}")
                result = None

            if result is not None:
                time.sleep(3)  # Optional: Wait for a short time before performing the action
                pyautogui.hotkey('alt', 'f4')
                time.sleep(1)

                print("      [*] Close button clicked!")
                return True  # Return True after attempting to close the game
            else:
                # print("  -Close button not found. Retrying in 10 seconds.")
                time.sleep(10)  # Wait for 10 seconds before checking again

    def __run_game(self):
        try:
            file = os.listdir(self.__replay_file_dir)[0]
            subprocess.run(
                ["start", "cmd", "/c", f"{self.__replay_file_dir}\{file}"], shell=True)
            return True
        except:
            return False

    def __select_player(self):
        if self.__player_team == 'Blue':
            # f1
            pydirectinput.keyDown('f3')
            pydirectinput.keyUp('f3')
            pydirectinput.keyDown(self.__player_index)
            pydirectinput.keyUp(self.__player_index)
            pydirectinput.keyDown(self.__player_index)
            pydirectinput.keyUp(self.__player_index)
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            # f2
            pydirectinput.keyDown('f3')
            pydirectinput.keyUp('f3')
            pydirectinput.keyDown(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyUp(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyDown(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyUp(
                keys[int(self.__player_index) - 1])
            
    def system_error_close(self):
        process_name = "League of Legends.exe"

        # Iterate over all running processes
        for proc in psutil.process_iter(['pid', 'name']):
            # Check if process name matches
            
            if proc.info['name'] == process_name:
                # Terminate the process
                print("   -",proc.info['name'])
                psutil.Process(proc.info['pid']).terminate()
                
                print(f"   -Terminated process {process_name} with PID {proc.info['pid']}")

    def close_game_setup(self):
        # target_window_title = "league of legends (TM) client"
        download_failed = "Download Failed"

        # Get a list of all open windows
        # open_windows = gw.getWindowsWithTitle(target_window_title)
        download_failed_window = gw.getWindowsWithTitle(download_failed)

        if download_failed_window:
            while True:
                print(f"   - {download_failed} is open.")
                logging.info(f"{download_failed} is open.")
                # Close the window

                download_failed_window = gw.getWindowsWithTitle(download_failed)
                if download_failed_window:
                    download_failed_window[0].close()
                    print(f"   -{download_failed} has been closed.")
                    logging.info(f"{download_failed} has been closed.")
                    time.sleep(5)
                    continue
                else:
                    break
        else:
            # print(f"   -{download_failed} is not open.")
            logging.info(f"{download_failed} is not open.")

        self.system_error_close()

if __name__ == '__main__':
    game_run_command = ['LeagueClient.exe']
    playerTeam = 'Blue'
    playerIndex = '1'
    controlGamePlay = ControlGamePlay(playerTeam, playerIndex, game_run_command)
    controlGamePlay.close_game()