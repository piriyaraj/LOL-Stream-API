from datetime import datetime
import json
import os
import shutil
import time


try:
    from utils.create_thumbnail import CreateThumbnail
    from utils.upload_youtube import UploadYoutube
except:
    from create_thumbnail import CreateThumbnail
    from upload_youtube import UploadYoutube
    


def moveVideo(sourceFolder, destFolder):
    count = 1
    try:
        if not os.path.exists(sourceFolder):
            return False

        os.makedirs(destFolder, exist_ok=True)
        file = os.listdir(sourceFolder)[-1]
        shutil.move(os.path.join(sourceFolder, file), os.path.join(destFolder, file))
        return True

    except Exception as e:
        if "being used by another process" in str(e) and count <= 3:
            count += 1
            time.sleep(10)
            moveVideo(sourceFolder, destFolder)

            
def move_all_files(youtube_record_path):
    # Move the most recent file to the "yt-temp" folder
    status = moveVideo(youtube_record_path, "yt-temp")
    if status == False:
        print(f"   [-] Recorded video failed to move")
        return
    # Create a new folder inside the "yt" folder named with the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_folder_path = os.path.join("yt", timestamp)
    os.makedirs(new_folder_path, exist_ok=True)

    # Move all files from "yt-temp" to the newly created folder
    for file in os.listdir("yt-temp"):
        shutil.move(os.path.join("yt-temp", file), os.path.join(new_folder_path, file))

    # print(f"Moved all files to '{new_folder_path}'")


def create_thumbnail(full_yt_folder):
    file_path = full_yt_folder + "/match_data.json"

    # Open the file and read its contents
    with open(file_path, "r") as file:
        data = json.load(file)  # Parse JSON data from the file
    if os.path.exists(os.path.join(full_yt_folder,"thumbnail.png")):
        return
    thumbnail_creator = CreateThumbnail(data,full_yt_folder)
    thumbnail_creator.create_thumbnail()
    pass

def upload_to_youtube(full_yt_folder):
    all_files = os.listdir(full_yt_folder)
    video_files = [file for file in all_files if file.endswith('.mkv') or file.endswith('.mp4')]
    
    thumbnail = os.path.join(full_yt_folder, 'thumbnail.png')
    matchData_path = os.path.join(full_yt_folder, 'match_data.json')
    videoPath = os.path.join(full_yt_folder, video_files[0])
    try:
        with open(matchData_path, 'r', encoding='utf-8') as matchData:
            match_data = json.load(matchData)
            uploader = UploadYoutube(match_data, videoPath, thumbnail)
            uploader.upload_video()
        shutil.rmtree(full_yt_folder)
    except Exception as e:
        print(f"yt_uploader(videoUploader): {str(e)}")



def run_youtube_upload():
    all_yt_folders =  os.listdir("yt")
    for yt_folder in all_yt_folders:
        full_yt_folder = os.path.abspath(os.path.join("yt",yt_folder))
        
        for file in os.listdir(full_yt_folder):
            if file.endswith(".mp4"):
                break
        else:
            is_today_created = str(yt_folder).split("_")[0] == datetime.now().strftime("%Y-%m-%d")
            if not is_today_created:
                shutil.rmtree(full_yt_folder)
        try:
            create_thumbnail(full_yt_folder)
        except:pass
        upload_to_youtube(full_yt_folder)

def youtube_runner():
    while True:
        run_youtube_upload()
        # print("hello world")
        time.sleep(60*10)
        
if __name__ == "__main__":
    youtube_runner()