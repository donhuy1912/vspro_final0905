from django.shortcuts import render, redirect
from homepage.models import EnviromentCate, UserRank,UserDetail
from homepage.myfunction import *
from datetime import datetime


# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userranks = UserRank.objects.all()
            for userrank in userranks:
                userrank.createdate = userrank.createdate
                userrank.editdate = userrank.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'userranks': userranks}
            return render(request, 'adminuserrank/userrank_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                # Lấy url của icon
                try:
                    token_icon = request.FILES['icon']
                except:
                    token_icon = None
                ico = ''
                if token_icon != None:
                    ico = tokenFile(token_icon)
                print('icon: ', ico)
                userrank = UserRank( 
                                        enviromentcateid=EnviromentCate.objects.get(enviromentcateid=request.POST['enviromentcateid']),
                                        userrankname=request.POST['userrankname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        icon=ico,
                                        requiredlevel=request.POST['requiredlevel'],  
                                        note=request.POST['note'])
                userrank.save()
                return redirect('/adminuserrank/')
            else:
                enviromentcates = EnviromentCate.objects.all()
                for enviromentcate in enviromentcates:
                    enviromentcate.createdate = enviromentcate.createdate
                    enviromentcate.editdate = enviromentcate.editdate

                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'enviromentcates': enviromentcates,
                }

                return render(request, 'adminuserrank/userrank_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userrank = UserRank.objects.get(userrankid = id)
            userrank.createdate = userrank.createdate
            userrank.editdate = datetime.now()

            enviromentcates = EnviromentCate.objects.all()
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'enviromentcates': enviromentcates,
                'userrank': userrank,
            }
            return render(request, 'adminuserrank/userrank_edit.html', context)
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
            userrank = UserRank.objects.get(userrankid=id)
            # Lấy url của icon
            try:
                token_icon = request.FILES['icon']
            except:
                token_icon = None
            ico = ''
            if token_icon != None:
                ico = tokenFile(token_icon)
            else:
                ico = userrank.icon
            userrank.enviromentcateid= EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid'])
            userrank.userrankname=request.POST['userrankname']
            userrank.createdate=userrank.createdate
            userrank.editdate=datetime.now()
            userrank.icon=ico
            userrank.requiredlevel=request.POST['requiredlevel']
            userrank.note=request.POST['note']
            userrank.save()
            return redirect('/adminuserrank/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userrank = UserRank.objects.get(userrankid= id)
            userrank.delete()
            return redirect('/adminuserrank/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')