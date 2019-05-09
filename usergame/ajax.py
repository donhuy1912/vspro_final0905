from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime

def ajaxforrate(request):
    idgame = request.GET.get('idgame')
    userrate = request.GET.get('userrate')

    account = Account.objects.get(username = request.session['username'])

    findgamerate = GameRate.objects.filter(gameid = idgame).filter(accountid = account)
    if len(findgamerate) > 0:
        for find in findgamerate:
            find.delete()
    
    game = Game.objects.get(gameid = idgame)

    gameratenew = GameRate(
        gameid = game,
        accountid = account,
        rate = userrate,
        createdate = datetime.now(),
        editdate = datetime.now()
    )
    gameratenew.save()
    sumrate=0
   
    gamerates = GameRate.objects.filter(gameid=game).order_by('-createdate')
    for gamerate in gamerates:
        sumrate += gamerate.rate
    countrate=len(gamerates)
    if countrate > 0:
        avgrate = round(sumrate/countrate, 2)
    else:
        countrate = 0
        avgrate = 0

    s =  str(avgrate) +' ( Bởi ' + str(countrate) + ' học viên )'
    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxfordelgame(request):
    idgame =request.GET.get('idgame')
    game=Game.objects.get(gameid=idgame)
    gamerates = GameRate.objects.filter(gameid=game)
    for gamerate in gamerates:
        gamerate.delete()
    game.delete()
    data = {

    }
    return JsonResponse(data)