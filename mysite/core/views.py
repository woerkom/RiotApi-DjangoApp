from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator
from .models import Match, Player_Match, Player
import requests
import json
from django.conf import settings


# Create your views here.
def MatchListView(request):

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

        return render(request, "boostrap_form.html", context)
    except Exception as e:
        return render(request, "boostrap_form.html", {'e':str(e)})

def Content(request):
    return render(
        request,
        "content.html",
        {
            'message' : "About HelloDjangoApp",
            'content' : "Example app page for Django."
        }
    )