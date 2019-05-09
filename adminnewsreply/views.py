from django.shortcuts import render, redirect
from homepage.models import NewsReply, News, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            newsreplys = NewsReply.objects.all()
            for newsreply in newsreplys:
                newsreply.createdate = newsreply.createdate
                newsreply.editdate = newsreply.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'newsreplys': newsreplys }
            return render(request, 'adminnewsreply/newsreply_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                newsreply = NewsReply( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        newsid = News.objects.get(newsid = request.POST['newsid']),
                                        content=request.POST['content'],
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                newsreply.save()
                return redirect('/adminnewsreply/')
            else:
                newss = News.objects.all()
                for news in newss:
                    news.createdate = news.createdate
                    news.editdate = news.editdate

                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'newss': newss,
                    'accounts': accounts,
                }
            return render(request, 'adminnewsreply/newsreply_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            newsreply = NewsReply.objects.get(newsreplyid=id)
            newsreply.createdate = newsreply.createdate
            newsreply.editdate = datetime.now()

            newss = News.objects.all()
            for news in newss:
                news.createdate = news.createdate
                news.editdate = news.editdate

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'newsreply': newsreply,
                'newss': newss,
                'accounts': accounts,
            }
            return render(request, 'adminnewsreply/newsreply_edit.html', context)
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
            newsreply = NewsReply.objects.filter(newsreplyid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            newsreply = NewsReply.objects.filter(newsreplyid = id).update(newsid = News.objects.get(newsid = getNum(request.POST['newsid'])))
            newsreply = NewsReply.objects.get(newsreplyid=id)
            newsreply.createdate=newsreply.createdate
            newsreply.editdate=datetime.now()
            newsreply.content=request.POST['content']
            newsreply.isenable=request.POST['isenable']
            newsreply.note=request.POST['note']
            newsreply.save()
            return redirect('/adminnewsreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            newsreply = NewsReply.objects.get(newsreplyid= id)
            newsreply.delete()
            return redirect('/adminnewsreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')