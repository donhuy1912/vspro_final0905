from django.shortcuts import render, redirect
from homepage.models import ForumReply, Forum, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumreplys = ForumReply.objects.all()
            for forumreply in forumreplys:
                forumreply.createdate = forumreply.createdate
                forumreply.editdate = forumreply.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'forumreplys': forumreplys }
            return render(request, 'adminforumreply/forumreply_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                forumreply = ForumReply( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        forumtopicid = Forum.objects.get(forumtopicid = request.POST['forumid']),
                                        content=request.POST['content'],
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                forumreply.save()
                return redirect('/adminforumreply/')
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
                    'accounts': accounts,
                }
            return render(request, 'adminforumreply/forumreply_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumreply = ForumReply.objects.get(forumreplyid=id)
            forumreply.createdate = forumreply.createdate
            forumreply.editdate = datetime.now()

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
                'forumreply': forumreply,
                'forums': forums,
                'accounts': accounts,
            }
            return render(request, 'adminforumreply/forumreply_edit.html', context)
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
            forumreply = ForumReply.objects.filter(forumreplyid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            forumreply = ForumReply.objects.filter(forumreplyid = id).update(forumtopicid = Forum.objects.get(forumtopicid = getNum(request.POST['forumid'])))
            forumreply = ForumReply.objects.get(forumreplyid=id)
            forumreply.createdate=forumreply.createdate
            forumreply.editdate=datetime.now()
            forumreply.status=request.POST['content']
            forumreply.isenable=request.POST['isenable']
            forumreply.note=request.POST['note']
            forumreply.save()
            return redirect('/adminforumreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forumreply = ForumReply.objects.get(forumreplyid= id)
            forumreply.delete()
            return redirect('/adminforumreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')