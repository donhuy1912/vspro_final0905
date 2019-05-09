from django.shortcuts import render, redirect
from homepage.models import EnviromentCate, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enviromentcates = EnviromentCate.objects.all()
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = enviromentcate.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'enviromentcates': enviromentcates}
            return render(request, 'adminenviromentcate/enviromentcate_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                enviromentcate = EnviromentCate( 
                                        enviromentcatename=request.POST['enviromentcatename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                enviromentcate.save()
                return redirect('/adminenviromentcate/')
            else:
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,}
                return render(request, 'adminenviromentcate/enviromentcate_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enviromentcate = EnviromentCate.objects.get(enviromentcateid=id)
            enviromentcate.createdate = enviromentcate.createdate
            enviromentcate.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'enviromentcate': enviromentcate}
            return render(request, 'adminenviromentcate/enviromentcate_edit.html', context)
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
            enviromentcate = EnviromentCate.objects.get(enviromentcateid=id)
            enviromentcate.enviromentcatename=request.POST['enviromentcatename']
            enviromentcate.createdate=enviromentcate.createdate
            enviromentcate.editdate=datetime.now()
            enviromentcate.isenable=request.POST['isenable']
            enviromentcate.note=request.POST['note']
            enviromentcate.save()
            return redirect('/adminenviromentcate/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enviromentcate = EnviromentCate.objects.get(enviromentcateid= id)
            enviromentcate.delete()
            return redirect('/adminenviromentcate/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')