# https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/FABFABFAB/EUW?api_key=
import requests  

def get_puuid(game_name,tag_line,api_key):
    header =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ta;q=0.8",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{api_key}"
        }
    end_point = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get( end_point, headers=header)
    if response.status_code == 200:
        return True,response.json()['puuid']
    else:
        return False, response.json()['status']['message']
    
def get_in_game_match_data(puuid,api_key):
    header =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ta;q=0.8",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{api_key}"
        }
    end_point = f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    response = requests.get( end_point, headers=header)
    if response.status_code == 200:
        return True,response.json()
    else:
        return False, response.json()['status']['message']
if __name__ == "__main__":
    print(get_puuid("Sinstinct","TMT","RGAPI-e402533c-0411-4121-ab3a-62001784ae2f"))