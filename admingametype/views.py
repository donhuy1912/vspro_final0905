from django.shortcuts import render, redirect
from homepage.models import GameType, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gametypes = GameType.objects.all()
            for gametype in gametypes:
                gametype.createdate = gametype.createdate
                gametype.editdate = gametype.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'gametypes': gametypes}
            return render(request, 'admingametype/gametype_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                gametype = GameType( 
                                        gametypename=request.POST['gametypename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now())
                gametype.save()
                return redirect('/admingametype/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,}
            return render(request, 'admingametype/gametype_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gametype = GameType.objects.get(gametypeid=id)
            gametype.createdate = gametype.createdate
            gametype.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'gametype': gametype}
            return render(request, 'admingametype/gametype_edit.html', context)
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
            gametype = GameType.objects.get(gametypeid=id)
            gametype.gametypename=request.POST['gametypename']
            gametype.createdate=gametype.createdate
            gametype.editdate=datetime.now()
            gametype.save()
            return redirect('/admingametype/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            gametype = GameType.objects.get(gametypeid= id)
            gametype.delete()
            return redirect('/admingametype/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')