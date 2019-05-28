from django.shortcuts import render,redirect
from django.core import serializers
from django.core.paginator import Paginator
from .models import Match, Player_Match, Player
import requests
import json
from django.conf import settings
from django.http import HttpResponseRedirect


# Create your views here.
def MatchListView(request):

    #VARIABLE PARA DEBUGEAR
    #settings.HEADERS["X-Riot-Token"] = 'RGAPI-39633240-eb60-44db-8dda-36cf28d9f419'

    url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/-uJykwfPEE98SClRH8f8mQs25DDWU85SnMMzDRPgGuzsk_k'

    try:
        r = requests.get(url, headers=settings.HEADERS)
        datos = r.json()
        matches = datos['matches']
        totalGames = datos['totalGames']

        #json.dumps(match)    para convertir dict en string
        l = [Match(json.dumps(match)) for match in matches]
        all_champions = list(l[0].champions.values())
        campeon_query = request.GET.get('champion')
        print("campeon:", campeon_query)
        if campeon_query != '' and campeon_query is not None:
            l = list(filter(lambda x: x.champion == campeon_query, l))
            totalGames = len(l)
        else:
            totalGames = datos['totalGames']
        
        paginator = Paginator(l, 8)
        page = request.GET.get('page')
        l = paginator.get_page(page)
        
        context = {
            'totalGames': totalGames,
            'matches': l,
            'championNames': all_champions  
        }

        request.session['my_thing'] = l[0].GetMatchInfo()[0].win
        #request.session['my_thing'] = {'266': 'Aatrox', '103': 'Ahri', '84': 'Akali',}


        return render(request, "boostrap_form.html", context)
    except Exception as e:
        #return render(request, "login.html", {"message": 'Token no válido: Probably your key has expired'})
        return render(request, "boostrap_form.html", {'e':str(e)})
        

def Login(request):
    if request.method == "POST":
        token = request.POST.get('password')
        settings.HEADERS["X-Riot-Token"] = token
        
        url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/kanuto1996'
        r = requests.get(url, headers=settings.HEADERS)
        datos = r.json()
        if 'status' in datos.keys():
            return render(request, "login.html", {"message": 'Token no válido: Probably your key has expired'})

        return redirect("matches/")

    else:
        return render(request, "login.html")


def ModalContent(request, gameId):
    #content = l[0].GetMatchInfo()[0].win
    #my_thing = request.session.get('my_thing', None) 
    context =   {
            'message' : gameId,
            'content' : "hola mundo"
        }
    return render(request, "content.html", context)