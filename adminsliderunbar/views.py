from django.shortcuts import render, redirect
from homepage.models import SlideRunBar, Account,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            sliderunbars = SlideRunBar.objects.all()
            for sliderunbar in sliderunbars:
                sliderunbar.createdate = sliderunbar.createdate
                sliderunbar.editdate = sliderunbar.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'sliderunbars': sliderunbars}
            return render(request, 'adminsliderunbar/sliderunbar_show.html', context)
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

                sliderunbar = SlideRunBar( 
                                        sliderunbarname=request.POST['sliderunbarname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        image=ima,  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                sliderunbar.save()
                return redirect('/adminsliderunbar/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,}
            return render(request, 'adminsliderunbar/sliderunbar_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            sliderunbar = SlideRunBar.objects.get(sliderunbarid=id)
            sliderunbar.createdate = sliderunbar.createdate
            sliderunbar.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'sliderunbar': sliderunbar}
            return render(request, 'adminsliderunbar/sliderunbar_edit.html', context)
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
            sliderunbar = SlideRunBar.objects.get(sliderunbarid=id)
            #Lấy url của image
            try:
                token_image = request.FILES['image']
            except:
                token_image = None
            ima = ''
            if token_image != None:
                ima = tokenFile(token_image)
            else:
                ima = sliderunbar.image
            
            sliderunbar.sliderunbarrname=request.POST['sliderunbarname']
            sliderunbar.createdate=sliderunbar.createdate
            sliderunbar.editdate=datetime.now()
            sliderunbar.content=request.POST['content']
            sliderunbar.link=request.POST['link']
            sliderunbar.image=ima
            sliderunbar.isenable=request.POST['isenable']
            sliderunbar.note=request.POST['note']
            sliderunbar.save()
            return redirect('/adminsliderunbar/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            sliderunbar = SlideRunBar.objects.get(sliderunbarid= id)
            sliderunbar.delete()
            return redirect('/adminsliderunbar/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')