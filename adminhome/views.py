from django.shortcuts import render, redirect
from homepage.models import Home, Account,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            homes = Home.objects.all()
            for home in homes:
                home.createdate = home.createdate
                home.editdate = home.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'homes': homes}
            return render(request, 'adminhome/home_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                #Lấy url của image
                try:
                    token_image = request.FILES['image']
                except:
                    token_image = None
                ima = ''
                if token_image != None:
                    ima = tokenFile(token_image)

                home = Home( 
                                        homename=request.POST['homename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        image=ima,  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                home.save()
                return redirect('/adminhome/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,}
            return render(request, 'adminhome/home_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            home = Home.objects.get(homeid=id)
            home.createdate = home.createdate
            home.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'home': home}
            return render(request, 'adminhome/home_edit.html', context)
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
            home = Home.objects.get(homeid=id)
                #Lấy url của image
            try:
                token_image = request.FILES['image']
            except:
                token_image = None
            ima = ''
            if token_image != None:
                ima = tokenFile(token_image)
            else:
                ima = home.image

            home.homename=request.POST['homename']
            home.createdate=home.createdate
            home.editdate=datetime.now()
            home.content=request.POST['content']
            home.link=request.POST['link']
            home.image=ima
            home.isenable=request.POST['isenable']
            home.note=request.POST['note']
            home.save()
            return redirect('/adminhome/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            home = Home.objects.get(homeid= id)
            home.delete()
            return redirect('/adminhome/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')