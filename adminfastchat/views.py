from django.shortcuts import render, redirect
from homepage.models import Account, FastChat, UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            fastchats = FastChat.objects.all()
            for fastchat in fastchats:
                fastchat.createdate = fastchat.createdate
                
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'fastchats': fastchats}
            return render(request, 'adminfastchat/fastchat_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                fastchat = FastChat( 
                                        accountid=Account.objects.get(accountid = request.POST['accountid']), 
                                        createdate= datetime.now(), 
                                        content= request.POST['content'], 
                                        isenable = request.POST['isenable'],
                                        note=request.POST['note'])
                fastchat.save()
                return redirect('/adminfastchat/')
            else:
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts}
            return render(request, 'adminfastchat/fastchat_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            fastchat = FastChat.objects.get(fastchatid=id)
            fastchat.createdate = fastchat.createdate
            
            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'fastchat': fastchat,
                'accounts': accounts,    
            }

            return render(request, 'adminfastchat/fastchat_edit.html', context)
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
            fastchat = FastChat.objects.get(fastchatid=id)
            fastchat.accountid=Account.objects.get(accountid = request.POST['accountid'])
            fastchat.createdate=fastchat.createdate
            fastchat.content=request.POST['content']
            fastchat.note=request.POST['note']
            fastchat.isenable=request.POST['isenable']
            fastchat.save()
            return redirect('/adminfastchat/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            fastchat = FastChat.objects.get(fastchatid= id)
            fastchat.delete()
            return redirect('/adminfastchat/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')