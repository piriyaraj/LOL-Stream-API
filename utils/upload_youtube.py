import re
import httplib2
import os
import random
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


class UploadYoutube:
    def __init__(self, match_data, video_file_name: str,thumbnail_file) -> None:
        self.__CLIENT_SECRETS_FILE = os.path.abspath("src/client_secrets.json")
        self.__YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner",
          "https://www.googleapis.com/auth/youtubepartner-channel-audit"]
        self.__YOUTUBE_API_SERVICE_NAME = "youtube"
        self.__YOUTUBE_API_VERSION = "v3"
        self.__VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
        self.__MISSING_CLIENT_SECRETS_MESSAGE = f"""
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

          {os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          self.__CLIENT_SECRETS_FILE))}

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """
        self.__thumb_file = thumbnail_file
        self.__file = video_file_name
        self.__get_authenticated_service()
        self.playlist_name_list = [match_data['mvp']['champion'],"Region "+match_data['region'],"Patch "+match_data['patch']]
        self.playlist_from_youtube = {}
        # self.__title = f"{match_data['mvp']['champion']} | {match_data['player_role']} vs {match_data['loser']} - {match_data['region']} {match_data['mvp']['rank']} Patch "

        self.__title = f"""{match_data['mvp']['name']} | {match_data['mvp']['champion']} VS {match_data['loser']} | FULL GAME | {match_data['date']}"""
        

        # self.__description = f"""
        # This is the match for {match_data['mvp']['champion']} in the Mid role. The match took place in the {match_data['region']} region. The patch used was {match_data['patch']}.

        # The match consisted of two teams. In Team 1, the players and their respective champions were:
        #     - {match_data['team1']['players'][0]['name']} playing {match_data['team1']['players'][0]['champion']} with a KDA of {match_data['team1']['players'][0]['kda']} and ranked as {match_data['team1']['players'][0]['rank']}. Their summoner spells were {self.extract_spell_name(match_data['team1']['players'][0]['spell'][0])}, {match_data['team1']['players'][0]['spell'][1]}.
        #     - {match_data['team1']['players'][1]['name']} playing {match_data['team1']['players'][1]['champion']} with a KDA of {match_data['team1']['players'][1]['kda']} and ranked as {match_data['team1']['players'][1]['rank']}. Their summoner spells were {self.extract_spell_name(match_data['team1']['players'][1]['spell'][0])}, {match_data['team1']['players'][1]['spell'][1]}.
        #     - {match_data['team1']['players'][2]['name']} playing {match_data['team1']['players'][2]['champion']} with a KDA of {match_data['team1']['players'][2]['kda']} and ranked as {match_data['team1']['players'][2]['rank']}. Their summoner spells were {self.extract_spell_name(match_data['team1']['players'][2]['spell'][0])}, {match_data['team1']['players'][2]['spell'][1]}.
        #     - {match_data['team1']['players'][3]['name']} playing {match_data['team1']['players'][3]['champion']} with a KDA of {match_data['team1']['players'][3]['kda']} and ranked as {match_data['team1']['players'][3]['rank']}. Their summoner spells were {self.extract_spell_name(match_data['team1']['players'][3]['spell'][0])}, {match_data['team1']['players'][3]['spell'][1]}.
        #     - {match_data['team1']['players'][4]['name']} playing {match_data['team1']['players'][4]['champion']} with a KDA of {match_data['team1']['players'][4]['kda']} and ranked as {match_data['team1']['players'][4]['rank']}. Their summoner spells were {self.extract_spell_name(match_data['team1']['players'][4]['spell'][0])}, {match_data['team1']['players'][4]['spell'][1]}.

        # The Most Valuable Player (MVP) of this match was {match_data['mvp']['name']} playing {match_data['mvp']['champion']} with a KDA of {match_data['mvp']['kda']} and ranked as {match_data['mvp']['rank']}. Their summoner spells were {self.extract_spell_name(match_data['mvp']['spell'][0])}, {match_data['mvp']['spell'][1]}.

        # The match resulted in a {match_data['team1']['result']} for Team 1.
        
        # league of legends new account, lol gameplay, league of legends videos, play league of legends, riot games lol, league of legends new season, twitch league of legends, riot games twitch, twitch lol, twitch tv league of legends, best jungler lol, pants are dragon lol, league of legends jungle, jungle guide, season jungle guide, best jungler for season, how to climb league of legends, pants are dragon season, pants are dragon jungle guide, pants are dragon rank 1, challenger to rank 1, pants are dragon rage, season league of legends, 
        
        # #LeagueOfLegends, #LoL, #SummonerRift, #Champions, #LeagueCommunity, #RankedGames, #ProPlay, #LCS, #Worlds, #Esports, #PatchNotes, #Gaming, #TeamfightTactics, #ARAM, #Streamer, #Pentakill, #Skins, #Lore, #Balance, #LeagueArt
        
        # """
        self.__description = """
Make sure to hit the like button and subscribe to my channel!

↓ MORE INFO ↓

Follow me:
👉 Twitch ► https://www.twitch.tv/spectate_baus
👉 Youtube ► https://www.youtube.com/channel/UC_yb6SvLnpDND_wRh9cEN3g
👉 Website ► https://www.spectatebaus.tv/

#Thebausffs #Babus #Simon #Spectate #Spectator #Full #Game #Highlight #LOL #Leagueoflegends #League #of #Legends #RIOTGAMES
        """
        self.__category = "20"
        self.__keywords = [f"{match_data['mvp']['champion']}", "challenger",
                           "leagueoflegends", "replay", "high kda",
                           f"{match_data['region']}"]
        httplib2.RETRIES = 1
        self.__MAX_RETRIES = 10
        self.__RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)
        self.__RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


    def extract_spell_name(self, url):
        match = re.search(r"/([^/]+)$", url)
        if match:
            return match.group(1)
        return ""
    
    def upload_video(self):
        try:
            self.__initialize_upload()
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    def __upload_thumbnail(self, youtube, video_id):
        # print('Uploading youtube thumnail...')
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=self.__thumb_file
        ).execute()

    def __build_video_data(self):
        return {
            "file": self.__file,
            "title": self.__title,
            "description": self.__description,
            "category": self.__category,
            "keywords": self.__keywords,
            "privacyStatus": self.__VALID_PRIVACY_STATUSES[0]
        }

    def progress_bar(self, progress):
        self.pbar.update(progress - self.pbar.n)

    def __get_authenticated_service(self):
        flow = flow_from_clientsecrets(self.__CLIENT_SECRETS_FILE,
                                       scope=self.__YOUTUBE_UPLOAD_SCOPE,
                                       message=self.__MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage(os.path.abspath("src/storage-oauth2.json"))
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(self.__YOUTUBE_API_SERVICE_NAME, self.__YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def __initialize_upload(self):
        youtube = self.__get_authenticated_service()
        options = self.__build_video_data()
        playlist_name_list = []
        tags = None
        if options['keywords']:
            tags = options['keywords']

        body = dict(
            snippet=dict(
                title=options['title'],
                description=options['description'],
                tags=tags,
                categoryId=options['category']
            ),
            status=dict(
                privacyStatus=options['privacyStatus']
            )
        )
        # Set chunksize to 1 MB  nochunk -1 it mean upload at once
        chunksize = -1

        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                options['file'], chunksize=chunksize, resumable=True)
        )

        video_id = self.__resumable_upload(insert_request)
        if os.path.exists(self.__thumb_file):
            self.__upload_thumbnail(youtube, video_id)
        # self.__add_video_to_playlist(video_id,playlist_name_list)
        
    def __resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            # print("=== Video uploading (wait until uploading finish) ===")
            try:
                # print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        # print(
                        #     f"Video id {response['id']} was successfully uploaded.")
                        return response['id']
                    else:
                        exit(
                            f"The upload failed with an unexpected response: {response}")
            except HttpError as e:
                if e.resp.status in self.__RETRIABLE_STATUS_CODES:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except self.__RETRIABLE_EXCEPTIONS as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > self.__MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)

    def __create_playlist(self,playListName,description):
        youtube = self.__get_authenticated_service()
        resource = {
            'snippet': {
                'title': playListName,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
        try:
            response = youtube.playlists().insert(
                part='snippet,status',
                body=resource
            ).execute()
            playlist_id = response['id']
            print(f"Playlist '{playListName}' created successfully with id '{playlist_id}'")
        except HttpError as error:
            print(f"An HTTP error {error.resp.status} occurred: {error.content}")
            playlist_id = None
        return playlist_id

    def __add_video_to_playlist(self,videoID,list_of_playlists):
        youtube = self.__get_authenticated_service()
        for playListName in list_of_playlists:
            playlistId = self.__check_playlist_id_in_database(playListName)
            add_video_request=youtube.playlistItems().insert(
                part="snippet",
                body={
                        'snippet': {
                        'playlistId': playlistId, 
                        'resourceId': {
                                'kind': 'youtube#video',
                            'videoId': videoID
                            }
                        #'position': 0
                        }
                }
            ).execute()

    def __check_playlist_id_in_database(self,playListName):
        database = Database()

        tag = playListName
        tag_id = database.getPlayListId(tag)
        if tag_id == None:
            tag_id = self.__check_playlist_name_in_youtube(tag)
            if tag_id is not None:   # if tag appear in youtube
                for idTemp,tagTemp in self.playlist_from_youtube.items():
                    database.setPlayListId(idTemp,tagTemp)
            else:
                description = f"""
                """
                time.sleep(10)
                tag_id = self.__create_playlist(tag,description=description)
            database.setPlayListId(tag_id,tag)
        return tag_id
    
    def remove_empty_kwargs(self,**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                if value:
                    good_kwargs[key] = value
        return good_kwargs

    def playlists_list_by_channel_id(self,client, **kwargs):
        kwargs = self.remove_empty_kwargs(**kwargs)

        response = client.playlists().list(*kwargs).execute()
        return response
    
    def __check_playlist_name_in_youtube(self,playlist_name):
        youtube = self.__get_authenticated_service()
        response = self.playlists_list_by_channel_id(youtube,part ='snippet, contentDetails',channelId ='UCwATXke_iLof1_OArUUwMTA',maxResults = 100)
        
        print(response)
        # add playlist and id in dictionary
        
        # check playlist exist then return id
        # else return None
        return None
        pass

