from django.shortcuts import render, redirect
from homepage.models import Header, Account,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            headers = Header.objects.all()
            for header in headers:
                header.createdate = header.createdate
                header.editdate = header.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,'headers': headers}
            return render(request, 'adminheader/header_show.html', context)
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
                    
                header = Header( 
                                        headername=request.POST['headername'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        image=ima,  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                header.save()
                return redirect('/adminheader/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,}
            return render(request, 'adminheader/header_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            header = Header.objects.get(headerid=id)
            header.createdate = header.createdate
            header.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'header': header}
            return render(request, 'adminheader/header_edit.html', context)
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
            header = Header.objects.get(headerid=id)
            #Lấy url của image
            try:
                token_image = request.FILES['image']
            except:
                token_image = None
            ima = ''
            if token_image != None:
                ima = tokenFile(token_image)
            else:
                ima = header.image

            
            header.headername=request.POST['headername']
            header.createdate=header.createdate
            header.editdate=datetime.now()
            header.content=request.POST['content']
            header.link=request.POST['link']
            header.image=ima
            header.isenable=request.POST['isenable']
            header.note=request.POST['note']
            header.save()
            return redirect('/adminheader/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            header = Header.objects.get(headerid= id)
            header.delete()
            return redirect('/adminheader/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')