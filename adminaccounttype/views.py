from django.shortcuts import render, redirect
from homepage.models import AccountType, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounttypes = AccountType.objects.all()
            for accounttype in accounttypes:
                #accounttype.createdate = accounttype.createdate.strftime("%Y-%m-%d")
                accounttype.createdate = accounttype.createdate
                accounttype.editdate = accounttype.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounttypes': accounttypes
                }
            return render(request, 'adminaccounttype/accounttype_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,}
            if request.method == 'POST':
                accounttype = AccountType( 
                                        accounttypename=request.POST['accounttypename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                accounttype.save()
                return redirect('/adminaccounttype/')

            return render(request, 'adminaccounttype/accounttype_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounttype = AccountType.objects.get(accounttypeid=id)
            accounttype.createdate = accounttype.createdate
            accounttype.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounttype': accounttype}
            return render(request, 'adminaccounttype/accounttype_edit.html', context)
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
            accounttype = AccountType.objects.get(accounttypeid=id)
            accounttype.accounttypename=request.POST['accounttypename']
            accounttype.createdate=accounttype.createdate
            accounttype.editdate=datetime.now()
            accounttype.isenable=request.POST['isenable']
            accounttype.note=request.POST['note']

        
            accounttype.save()
            return redirect('/adminaccounttype/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 
   


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounttype = AccountType.objects.get(accounttypeid= id)
            accounttype.delete()
            return redirect('/adminaccounttype/')
            #return redirect('/crud/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 