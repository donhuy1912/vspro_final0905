from django.shortcuts import render, redirect
from homepage.models import Footer, Account,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            footers = Footer.objects.all()
            for footer in footers:
                footer.createdate = footer.createdate
                footer.editdate = footer.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'footers': footers}
            return render(request, 'adminfooter/footer_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request): 
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:       
            #Lấy url của image
            try:
                token_image = request.FILES['image']
            except:
                token_image = None
            ima = ''
            if token_image != None:
                ima = tokenFile(token_image)
            
            if request.method == 'POST':
                footer = Footer( 
                                        footername=request.POST['footername'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        image=ima,  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                footer.save()
                return redirect('/adminfooter/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,}
            return render(request, 'adminfooter/footer_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1: 
            footer = Footer.objects.get(footerid=id)
            footer.createdate = footer.createdate
            footer.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'footer': footer}
            return render(request, 'adminfooter/footer_edit.html', context)
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
            footer = Footer.objects.get(footerid=id)
            #Lấy url của image
            try:
                token_image = request.FILES['image']
            except:
                token_image = None
            ima = ''
            if token_image != None:
                ima = tokenFile(token_image)
            else:
                ima = footer.image

            footer.footername=request.POST['footername']
            footer.createdate=footer.createdate
            footer.editdate=datetime.now()
            footer.content=request.POST['content']
            footer.link=request.POST['link']
            footer.image=ima
            footer.isenable=request.POST['isenable']
            footer.note=request.POST['note']
            footer.save()
            return redirect('/adminfooter/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            footer = Footer.objects.get(footerid= id)
            footer.delete()
            return redirect('/adminfooter/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')