from django.db import models
import json
import datetime
import requests
from django.conf import settings

# Create your models here.
class Player_Match(object):
    def __init__(self, gameId, player_info):
        self.gameId = gameId
        #Mas tarde puedo crear un objeto estadisticas e importarme todas las estadísticas de stats.
        self.win = player_info['stats']['win']
        self.kills = player_info['stats']['kills']
        self.deaths = player_info['stats']['deaths']
        self.assists = player_info['stats']['assists']
        self.champion = Match.GetChampionName(player_info['championId'])

        self.player = Player(player_info['player'])

class Player(object):
    def __init__(self, player_info):
        for key in player_info: #forma de pasar de un dict a una clase
            setattr(self, key, player_info[key])

class Match(object):
    
    champions=[] #atributo compartido entre los objetos de la clase
    
    def Timestamp_toDate(self):
        self.timestamp = datetime.datetime.fromtimestamp(self.timestamp/1000)
        self.timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def GetAllChampionsName():
        url = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json' 
        r = requests.get(url, headers=settings.HEADERS)
        datos = r.json()
        champions = datos['data']
        return {champions[champ]['key'] : champions[champ]['id'] for champ in champions}

    @staticmethod
    def GetChampionName(champion):
        champions = Match.GetAllChampionsName()
        if str(champion) in champions:
            return champions[str(champion)]
        else:
            return champion
    def GetMatchInfo(self): #de repente si lo quito: "object has no attribute GetMathInfo()" aunque no lo estoy usando.
        url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + str(self.gameId)
        r = requests.get(url, headers=settings.HEADERS)
        datos = r.json()
        playersMatch = []
        for i in range(10):
            player_info = {**datos['participantIdentities'][i], **datos['participants'][i]} #Info de un jugador en una partida
            playersMatch.append(Player_Match(self.gameId, player_info)) 
        return playersMatch
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self.Timestamp_toDate()
        if not self.champions:
            self.champions = self.GetAllChampionsName()
        self.champion = self.GetChampionName(self.champion)
        