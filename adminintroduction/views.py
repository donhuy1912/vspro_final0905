from django.shortcuts import render, redirect
from homepage.models import *
from datetime import datetime
from homepage.myfunction import tokenFile
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            introductions = Introduction.objects.all()

            for introduction in introductions:
                introduction.createdate = introduction.createdate
                introduction.editdate = introduction.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'introductions': introductions}

            return render(request, 'adminintroduction/introduction_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                # Lấy url của image
                try:
                    token_image = request.FILES['image']
                except:
                    token_image = None
                ima = ''
                if token_image != None:
                    ima = tokenFile(token_image)

                introduction = Introduction( 
                                        introductionname=request.POST['introductionname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        image=ima,  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                introduction.save()
                return redirect('/adminintroduction/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,}
            return render(request, 'adminintroduction/introduction_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
    
def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            introduction = Introduction.objects.get(introductionid=id)
            introduction.createdate = introduction.createdate
            introduction.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'introduction': introduction}
            return render(request, 'adminintroduction/introduction_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def getNum(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            introduction = Introduction.objects.get(introductionid=id)
            if request.method == 'POST':
                # Lấy url của image
                try:
                    token_image = request.FILES['image']
                except:
                    token_image = None
                ima = ''
                if token_image != None:
                    ima = tokenFile(token_image)
                else:
                    ima = introduction.image
            
            introduction.introductionname=request.POST['introductionname']
            introduction.createdate=introduction.createdate
            introduction.editdate=datetime.now()
            introduction.content=request.POST['content']
            introduction.link=request.POST['link']
            introduction.image=ima
            introduction.isenable=request.POST['isenable']
            introduction.note=request.POST['note']
            introduction.save()
            return redirect('/adminintroduction/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            introduction = Introduction.objects.get(introductionid= id)
            introduction.delete()
            return redirect('/adminintroduction/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')