from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.
def userforum(request):
    islog = 0
    forums = Forum.objects.all().order_by('-createdate')
    enviromentcates = EnviromentCate.objects.all()

    userdetailforumlist = []
    for forum in forums:
        userdetail =  UserDetail.objects.get(accountid = forum.accountid)
        temp = ForumUserdetail(forum, userdetail)
        userdetailforumlist.append(temp)
    header = Header.objects.get(headername = 'forum')
    
    # Quy định cách hiển thị table forum khi chưa đăng nhập
    classdiv = "col-lg-12"

    #Chia trang
    # paginator = Paginator(userdetailforumlist, 10) # Show 25 contacts per page
    # page = request.GET.get('page')
    # userdetailforumlist = paginator.get_page(page)    

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        
        # load các bài viết của user
        yourforums = Forum.objects.filter(accountid = account.accountid).order_by('-createdate')
        lenyourfor = len(yourforums)
        if lenyourfor>4:
            yourforums = yourforums[0:4]

        # load các bài viết mà user tương tác
        forumreplys = ForumReply.objects.filter(accountid = account.accountid).order_by('-createdate')
        lenforrep = len(forumreplys)
        if lenforrep>4:
            forumreplys = forumreplys[0:4]

        # Quy định cách hiển thị table forum khi đã đăng nhập
        classdiv = "col-lg-9"

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'forums': forums,
            'userdetailforumlist': userdetailforumlist,
            'yourforums': yourforums,
            'forumreplys': forumreplys,
            'lenyourfor': lenyourfor,
            'lenforrep': lenforrep,
            'classdiv': classdiv,
            'header': header,
        }
        return render(request, 'userforum/userforum.html', context)

    context = {
        'islog': islog,
        'enviromentcates': enviromentcates,
        'forums': forums,
        'userdetailforumlist': userdetailforumlist,
        'classdiv': classdiv,
        'header': header,
    }
    return render(request, 'userforum/userforum.html', context)
 
def userforumblog(request, id):
    islog = 0
    forum = Forum.objects.get(forumtopicid = id)
    like = 0
    forum.viewcount +=1
    forum.save()

    likeCount = getlikeForumId(forum)

    forumreplys = ForumReply.objects.filter(forumtopicid = forum).order_by('-createdate')
    userdetailforumreplylist = []
    for forumreply in forumreplys:
        forumreply.forumreplyid = 'CommentDelete(' + str(forumreply.forumreplyid) + ')'
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        temp = ForumReplyUserdetail(forumreply, userdetail)
        userdetailforumreplylist.append(temp)
    lenforumreplys = len(forumreplys)

    popularforums = Forum.objects.filter(subjectid = None).order_by('-viewcount')
    popularforums = popularforums[0:4]

    relativeforums = Forum.objects.filter(subjectid = None).filter(enviromentcateid = forum.enviromentcateid).order_by('-createdate')
    relativeforums = relativeforums[0:4]

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        usename = request.session['username']
        if checkLikeForum(id, usename):
            like = 1
        
        context = {
            'islog': islog,
            'forum': forum,
            'account':account,
            'userdetailforumreplylist': userdetailforumreplylist,
            'forumreplys': forumreplys,
            'lenforumreplys': lenforumreplys,
            'popularforums': popularforums,
            'relativeforums': relativeforums,
            'likeCount': likeCount,
            'like': like,
        }
    
        return render(request, 'userforum/userforumblog.html', context)

    context = {
        'forum': forum,
        'islog': islog,
        'userdetailforumreplylist': userdetailforumreplylist,
        'forumreplys': forumreplys,
        'lenforumreplys': lenforumreplys,
        'popularforums': popularforums,
        'relativeforums': relativeforums,
        'likeCount': likeCount,
        'like': like,
    }
    return render(request, 'userforum/userforumblog.html', context)

def userforumpost(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()

        if request.method == "POST":
            enviromentcateid = request.POST.get('enviromentcateid')
            forumtopicname = request.POST.get('forumtopicname')
            description = request.POST.get('description')
            content = request.POST.get('content')
            try:
                avatar = request.FILES.get('avatar')
            except:
                avatar = None
            if avatar != None:
                ava = tokenFile(avatar)
            else:
                ava = ''
            note = request.POST.get('note')

            forum = Forum(
                enviromentcateid = EnviromentCate.objects.get(enviromentcateid = enviromentcateid),
                accountid = account,
                forumtopicname = forumtopicname,
                description = description,
                content = content,
                createdate = datetime.now(),
                editdate = datetime.now(),
                avatar = ava,
                viewcount = 0,
                likecount = 0,
                isenable = 1,
                note = note,
            )
            forum.save()
            context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            }
            return redirect('userforum:userforum')



        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
        }
        return render(request, 'userforum/userforumpost.html', context)
    else:  
        context = {
            'islog': islog,
        }
        return redirect('homepage:index')

def fastchat(request):
    lastid=0
    faschats= FastChat.objects.all().order_by("fastchatid")
    lenfc =len(faschats)
    if lenfc > 15:
        faschats=faschats[lenfc-15:lenfc]
    lenfc =len(faschats)
    if lenfc > 0:
        lastid=faschats[lenfc-1].fastchatid
    
    if request.session.has_key('username'):
        islog = 1    
        account = Account.objects.get(username = request.session['username'])
        context = {
            'faschats':faschats,
            'lastid':lastid,
            'islog': islog,
            'account': account
        }
        return render(request, 'userforum/fastchat.html', context)
    else:
        islog = 0
        context = {
            'faschats':faschats,
            'lastid':lastid,
            'islog': islog,
        }
        return render(request, 'userforum/fastchat.html', context)

def myuserforum(request, id):
    islog = 0
    enviromentcates = EnviromentCate.objects.all()    

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        forums = Forum.objects.filter(accountid = account.accountid).order_by('-createdate')
        forums = forums[0:9]

        userdetailforumlist = []
        for forum in forums:
            userdetail =  UserDetail.objects.get(accountid = forum.accountid)
            temp = ForumUserdetail(forum, userdetail)
            userdetailforumlist.append(temp)
        header = Header.objects.get(headername = 'forum')
        #Chia trang
        # paginator = Paginator(userdetailforumlist, 10) # Show 25 contacts per page
        # page = request.GET.get('page')
        # userdetailforumlist = paginator.get_page(page)
        
        # # load các bài viết của user
        # yourforums = Forum.objects.filter(accountid = account.accountid).order_by('-createdate')
        # yourforums = yourforums[0:4]

        # # load các bài viết mà user tương tác
        # forumreplys = ForumReply.objects.filter(accountid = account.accountid).order_by('-createdate')
        # forumreplys = forumreplys[0:4]

        # Quy định cách hiển thị table forum khi đã đăng nhập
        classdiv = "col-lg-9"

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'forums': forums,
            'userdetailforumlist': userdetailforumlist,
            'classdiv': classdiv,
            'header': header,
        }
        return render(request, 'userforum/myuserforum.html', context)

    return redirect('homepage:index')

def myuserforumpost(request, id):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()
        subjects = Subject.objects.all()

        if request.method == "POST":
            enviromentcateid = request.POST.get('enviromentcateid')
            description = request.POST.get('description')
            if request.POST.get('subjectid') != '0':
                subjectid = Subject.objects.get(subjectid = request.POST.get('subjectid'))
            else:
                subjectid = None

            forumtopicname = request.POST.get('forumtopicname')
            content = request.POST.get('content')
            try:
                avatar = request.FILES.get('avatar')
            except:
                avatar = None
            if avatar != None:
                ava = tokenFile(avatar)
            else:
                ava = ''
            note = request.POST.get('note')

            forum = Forum(
                enviromentcateid = EnviromentCate.objects.get(enviromentcateid = enviromentcateid),
                accountid = account,
                subjectid = subjectid,
                forumtopicname = forumtopicname,
                description = description,
                content = content,
                createdate = datetime.now(),
                editdate = datetime.now(),
                avatar = ava,
                viewcount = 0,
                likecount = 0,
                isenable = 1,
                note = note,
            )
            forum.save()
        
            return redirect('userforum:myuserforum', account.accountid)

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'subjects': subjects,
            }
        return render(request, 'userforum/myuserforumpost.html', context)
    else:  
        return redirect('homepage:index')

def myuserforumedit(request, idacc, idfor):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        forum = Forum.objects.get(forumtopicid = idfor)
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()
        subjects = Subject.objects.all()

        if request.method == "POST":
            enviromentcateid = request.POST.get('enviromentcateid')
            description = request.POST.get('description')
            if request.POST.get('subjectid') != '0':
                subjectid = request.POST.get('subjectid')
            else:
                subjectid = None

            forumtopicname = request.POST.get('forumtopicname')
            content = request.POST.get('content')
            try:
                avatar = request.FILES.get('avatar')
            except:
                avatar = None
            if avatar != None:
                ava = tokenFile(avatar)
            else:
                ava = ''
            note = request.POST.get('note')

            
            # if(enviromentcateid != forum.enviromentcateid.enviromentcateid):
            forum = Forum.objects.filter(forumtopicid = idfor).update(enviromentcateid = enviromentcateid)
            forum = Forum.objects.filter(forumtopicid = idfor).update(subjectid = subjectid)
            forum = Forum.objects.filter(forumtopicid = idfor).update(forumtopicname = forumtopicname)
            forum = Forum.objects.filter(forumtopicid = idfor).update(editdate = datetime.now())
            forum = Forum.objects.filter(forumtopicid = idfor).update(description = description)
            forum = Forum.objects.filter(forumtopicid = idfor).update(content = content)
            forum = Forum.objects.filter(forumtopicid = idfor).update(note = note)
            
            
            
            return redirect('userforum:myuserforum', account.accountid)

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'subjects': subjects,
            'forum': forum,
            }
        return render(request, 'userforum/myuserforumedit.html', context)
    else:  
        return redirect('homepage:index')