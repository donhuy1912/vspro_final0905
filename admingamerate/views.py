from django.shortcuts import render, redirect
from homepage.models import GameRate, Account, Game,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gamerates = GameRate.objects.all()
            for gamerate in gamerates:
                gamerate.createdate = gamerate.createdate
                gamerate.editdate = gamerate.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'gamerates': gamerates}
            return render(request, 'admingamerate/gamerate_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                gamerate = GameRate( 
                                        accountid= Account.objects.get(accountid = request.POST['accountid']), 
                                        gameid= Game.objects.get(gameid = request.POST['gameid']), 
                                        rate= request.POST['rate'],
                                        editdate=datetime.now(),  
                                        createdate=datetime.now())
                gamerate.save()
                return redirect('/admingamerate/')
            else:
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                games = Game.objects.all()
                for game in games:
                    game.createdate = game.createdate
                    game.editdate = game.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts,
                    'games': games,
                }
            return render(request, 'admingamerate/gamerate_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gamerate = GameRate.objects.get(gamerateid=id)
            gamerate.createdate = gamerate.createdate
            gamerate.editdate = datetime.now()

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            
            games = Game.objects.all()
            for game in games:
                game.createdate = game.createdate
                game.editdate = game.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'gamerate': gamerate,
                'games': games,
                'accounts': accounts,
            }
            return render(request, 'admingamerate/gamerate_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def us_date_to_iso(us_date):
    return '{2}-{0:>02}-{1:>02}'.format(*us_date.split('/'))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gamerate = GameRate.objects.get(gamerateid=id)
            gamerate.gameid = Game.objects.get(gameid = request.POST['gameid'])
            gamerate.accountid = Account.objects.get(accountid = request.POST['accountid'])
            gamerate.rate = request.POST['rate']
            gamerate.createdate=gamerate.createdate
            gamerate.editdate=datetime.now()

            gamerate.save()
            return redirect('/admingamerate/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gamerate = GameRate.objects.get(gamerateid= id)
            gamerate.delete()
            return redirect('/admingamerate/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')