from selenium import webdriver

from io import BytesIO
from PIL import Image
import os
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
try:
    from utils.data_scrapper import DataScrapper as scrapper
except:
    from data_scrapper import DataScrapper as scrapper

def iconReplace(champion):
    name = champion.replace(" ","")
    name = name.replace("'","")
    name = name.replace("&","")
    # print("Champion",name)
    if (name == "KaiSa"):
        return "Kaisa"
    elif (name == "VelKoz"):
        return "Velkoz"
    elif (name == "KhaZix"):
        return "Khazix"
    elif (name == "NunuWillump"):
        return "Nunu"
    elif (name == "BelVeth"):
        return "Belveth"
    elif (name == "RenataGlasc"):
        return "Renata"
    elif (name == "RekSai"):
        return "RekSai"
    elif (name == "Wukong"):
        return "MonkeyKing"
    elif (name == "Dr.Mundo"):
        return "DrMundo"
    else:
        return name


class CreateThumbnail:
    def __init__(self, data,folder) -> None:
        self.scrapper = scrapper(headless=True)
        self.driver = self.scrapper.driver

        self.lol_data = data
        self.folder = folder
        self.__thumb_path = os.path.join(self.folder, 'thumbnail.png')

        self.total = 100
        #print_progress(1, self.total, prefix='   > Creating Thumbnail:')
        self.skins = {
            "Yuumi": [0, 1, 11, 19, 28, 37, 39],
        }

    def exceptionHandle(self, name):
        # print(name)
        if (name == "AurelionSol"):
            return "aurelion-sol"
        elif (name == "KaiSa"):
            return "Kai-sa"
        elif (name == "VelKoz"):
            return "vel-koz"
        elif (name == "KhaZix"):
            return "kha-zix"
        elif (name == "NunuWillump"):
            return "Nunu"
        elif (name == "BelVeth"):
            return "bel-veth"
        elif (name == "RenataGlasc"):
            return "Renata"
        elif (name == "TwistedFate"):
            return "Twisted-fate"
        elif (name == "LeeSin"):
            return "lee-sin"
        elif (name == "RekSai"):
            return "rek-sai"
        elif (name == "KSante"):
            return "k-sante"
        elif (name == "KogMaw"):
            return "Kog-maw"
        elif (name == "JarvanIV"):
            return "jarvan-iv"
        elif (name == "MasterYi"):
            return "Master-yi"
        elif (name == "Dr.Mundo"):
            return "dr-mundo"
        elif (name == "Dr.Mundo"):
            return "dr-mundo"
        else:
            return name

    def iconReplace(self, champion):
        name = champion.replace(" ","")
        if (name == "KaiSa"):
            return "Kaisa"
        elif (name == "VelKoz"):
            return "Velkoz"
        elif (name == "KhaZix"):
            return "Khazix"
        elif (name == "NunuWillump"):
            return "Nunu"
        elif (name == "BelVeth"):
            return "Belveth"
        elif (name == "RenataGlasc"):
            return "Renata"
        elif (name == "RekSai"):
            return "RekSai"
        elif (name == "Wukong"):
            return "MonkeyKing"
        elif (name == "Dr.Mundo"):
            return "DrMundo"
        else:
            return name

    def getSkin(self, name):
        # url = "https://www.leagueoflegends.com/en-gb/champions/{name}/"
        # make get request and use beautifulsoup and find the skin img urls
        url = "https://www.leagueoflegends.com/en-gb/champions/{}/".format(
            name)
        # print(url)
        r = requests.get(url)
        # if r.status_code is '404':
        #     url = "https://www.leagueoflegends.com/en-pl/champions/{}/".format(name)
        #     r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        skinsImgTag = soup.find_all('img')
        skinsUrls = list(set([skin.get('src') for skin in skinsImgTag]))
        filtered_urls = [
            skinUrl for skinUrl in skinsUrls if skinUrl is not None and "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/" in skinUrl]

        return filtered_urls

    def change_champion_name(self,champion):
        champion = champion.replace("'", "& ")
        champion = champion.replace("&", "")
        if (len(champion.split()) == 2):
            champion = champion.replace(" ", "-")
        
        champion = champion.replace(" ", "").lower()

        return champion

    def create_thumbnail(self):
        #print_progress(5, self.total, prefix='   > Creating Thumbnail:')
        champion = self.lol_data['mvp']['champion']
        championRaw = champion
        champion = self.change_champion_name(champion)
        championTemp = champion
        champion = self.exceptionHandle(champion)
        #print_progress(8, self.total, prefix='   > Creating Thumbnail:')
        # if champion=="KaiSa":
        #     champion=="Kaisa"
        rank = self.lol_data['mvp']['rank']
        ranks = {
            "iron": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png",
            "bronze": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png",
            "silver": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png",
            "gold": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png",
            "platinum": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png",
            "emerald": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png",
            "diamond": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png",
            "master": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png",
            "grandMaster": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png",
            "challenger": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/10.png"
        }
        #print_progress(12, self.total, prefix='   > Creating Thumbnail:')
        # print(rank)
        rankIcon = ranks.get(rank.lower().strip())
        if (rankIcon is None):
            rankIcon = "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        spellImgs = os.listdir("src/img/spell")
        #print_progress(19, self.total, prefix='   > Creating Thumbnail:')
        spellImg = random.sample(spellImgs, 3)
        spellImgNew = self.lol_data['mvp']['spell']
        spellImgNew = [s+'.png' for s in spellImgNew]
        spellImg = spellImgNew
        #print_progress(25, self.total, prefix='   > Creating Thumbnail:')

        loser = self.lol_data['loser']
        imgUrl = ""
        count = 0
        # print(champion)
        # print("match region:",self.lol_data['region'],os.path.exists(f"assets/img/{self.lol_data['region']}.png"))
        if (os.path.exists(f"src/img/{self.lol_data['region']}.png")):
            region = self.lol_data['region']
        else:
            region = "EUW"
        skins = self.getSkin(champion)
        # print(skins)
        if (len(skins) == 0):
            print("\n==> Thumbnail creation failed \n==> Sent message to developer!\n==> Take a screenshot and sent mail to : tamilcomway@gmail.com")
            # print("==> Champion Temp: " + champonTemp)
            print("==> Champion name: " + str(champion))
            print("==> Raw Champion name: " + str(championRaw))
            print("==> URL:", imgUrl)
            self.scrapper.quit()
            return False
        imgUrl = random.choice(skins)

        #print_progress(40, self.total, prefix='   > Creating Thumbnail:')
        oppIconImg = iconReplace(championRaw)
        loserIcon = iconReplace(loser)
        self.__create_html(
            date=self.lol_data['date'],
            imgUrl=imgUrl,
            mvp=self.lol_data['mvp']['name'],
            vs=self.lol_data['loser'],
            rank=rank.upper(),
            patch=self.lol_data['patch'],
            rankIcon=rankIcon,
            spellImg=spellImg,
            opponentIcon=f'https://opgg-static.akamaized.net/meta/images/lol/14.11.1/champion/{oppIconImg}.png',
            region=region,
            loserIcon=f'https://opgg-static.akamaized.net/meta/images/lol/14.11.1/champion/{loserIcon}.png',
        )
        #print_progress(50, self.total, prefix='   > Creating Thumbnail:')
        html_path = os.path.abspath('src/thumbnail.html')
        self.driver.get('file://' + html_path)
        timer = 51
        for i in range(10):
            sleep(0.5)
            #print_progress(timer+i*2, self.total, prefix='   > Creating Thumbnail:')
        self.driver.set_window_size(1280, 805)
        #print_progress(81, self.total, prefix='   > Creating Thumbnail:')
        screenshot = self.driver.get_screenshot_as_png()
        #print_progress(91, self.total, prefix='   > Creating Thumbnail:')
        with Image.open(BytesIO(screenshot)) as img:
            img = img.convert('RGB')
            img = img.resize((1280, 720))
            img.save(self.__thumb_path, quality=70)
            # img.save(self.__static_thumb_path, quality=70)
        #print_progress(100, self.total, prefix='   > Creating Thumbnail:')
        self.scrapper.quit()

        return True

    def __create_html(self, date: str, mvp: str, vs: str, rank: str, patch: str, imgUrl: str, rankIcon: str, spellImg: list, opponentIcon: str, region, loserIcon):
        none_vars = []
        if date is None:
            none_vars.append('kda')
        if mvp is None:
            none_vars.append('mvp')
        if vs is None:
            none_vars.append('vs')
        if rank is None:
            none_vars.append('rank')
        if patch is None:
            none_vars.append('patch')
        if imgUrl is None:
            none_vars.append('imgUrl')
        if rankIcon is None:
            none_vars.append('rankIcon')
        if spellImg is None:
            none_vars.append('spellImg')
        if none_vars:
            # print(f"One or more arguments are None: {', '.join(none_vars)}")
            return
        with open("./src/template.html", "r", encoding='utf-8') as f:
            HTML = f.read()
            # print(HTML)
        HTML = HTML.replace("backgroundImageLOL", imgUrl.replace("'", ""))
        HTML = HTML.replace("rankIconLOL", rankIcon)
        HTML = HTML.replace("loserIconLOL", loserIcon)
        HTML = HTML.replace("opponentIconLOL", opponentIcon)
        HTML = HTML.replace("patchLOL", patch)
        HTML = HTML.replace("rankLOL", rank)
        HTML = HTML.replace("regionLOL", region)
        HTML = HTML.replace("spellImg0LOL", spellImg[0])
        HTML = HTML.replace("spellImg1LOL", spellImg[1])
        HTML = HTML.replace("mvpLOL", mvp)
        HTML = HTML.replace("kda0LOL", date)
        # HTML = HTML.replace("kda1LOL", kda[1])
        # HTML = HTML.replace("kda2LOL", kda[2])

        with open("./src/thumbnail.html", "w", encoding='utf-8') as f:
            f.write(HTML)


if __name__ == "__main__":
    from data import load
    lol_data: MatchData = load()
    driver = webdriver.Firefox()
    thumb_creator = CreateThumbnail(driver, data=lol_data)
    thumb_creator.create_thumbnail()
