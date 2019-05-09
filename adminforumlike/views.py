from django.shortcuts import render, redirect
from homepage.models import ForumLike, Forum, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumlikes = ForumLike.objects.all()
            
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'forumlikes': forumlikes }
            return render(request, 'adminforumlike/forumlike_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                forumlike = ForumLike( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        forumtopicid = Forum.objects.get(forumtopicid = request.POST['forumid']),
                                        status=request.POST['status'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                forumlike.save()
                return redirect('/adminforumlike/')
            else:
                forums = Forum.objects.all()
                for forum in forums:
                    forum.createdate = forum.createdate
                    forum.editdate = forum.editdate
                
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'forums': forums,
                    'accounts': accounts
                }
            return render(request, 'adminforumlike/forumlike_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumlike = ForumLike.objects.get(forumlikeid=id)
            forums = Forum.objects.all()
            for forum in forums:
                forum.createdate = forum.createdate
                forum.editdate = forum.editdate

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'forumlike': forumlike,
                'forums': forums,
                'accounts': accounts,
            }
            return render(request, 'adminforumlike/forumlike_edit.html', context)
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
            forumlike = ForumLike.objects.filter(forumlikeid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            forumlike = ForumLike.objects.filter(forumlikeid = id).update(forumtopicid = Forum.objects.get(forumtopicid = getNum(request.POST['forumid'])))
            forumlike = ForumLike.objects.get(forumlikeid=id)
            forumlike.status=request.POST['status']
            forumlike.isenable=request.POST['isenable']
            forumlike.note=request.POST['note']
            forumlike.save()
            return redirect('/adminforumlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumlike = ForumLike.objects.get(forumlikeid= id)
            forumlike.delete()
            return redirect('/adminforumlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')