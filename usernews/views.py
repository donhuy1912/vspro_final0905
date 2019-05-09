from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator

def usernews(request):
    islog = 0
    newss = News.objects.all().order_by('-createdate')

    header = Header.objects.get(headername = 'News')

    userdetailnewslist = []
    for news in newss:
        userdetail =  UserDetail.objects.get(accountid = news.accountid)
        temp = NewsUserdetail(news, userdetail)
        userdetailnewslist.append(temp)
    

    # Chia trang
    # paginator = Paginator(userdetailnewslist, 10) # Show 25 contacts per page
    # page = request.GET.get('page')
    # userdetailnewslist = paginator.get_page(page)
    
    
    if request.session.has_key('username'):
        username = request.session['username']
        account = Account.objects.get(username = username)
        islog = 1
        context = {
        'newss': newss,
        'islog': islog,
        'username': username,
        'userdetailnewslist': userdetailnewslist,
        'account': account,
        'header': header,
        }
        return render(request, 'usernews/usernews.html', context)
    context = {
        'newss': newss,
        'islog': islog,
        'userdetailnewslist': userdetailnewslist,
        'header': header,
    }
    return render(request, 'usernews/usernews.html', context)

def usernewsblog(request, id):
    islog = 0
    newss = News.objects.all().order_by('createdate')
    newss = newss[0:10]

    news = News.objects.get(newsid = id)

    newsreplys = NewsReply.objects.filter(newsid = id).order_by('-createdate')
    lennewsrep = len(newsreplys)

    userdetailnewsreplylist = []
    for newsreply in newsreplys:
        newsreply.newsreplyid = 'CommentDelete(' + str(newsreply.newsreplyid) + ')'
        userdetail =  UserDetail.objects.get(accountid = newsreply.accountid)
        temp = NewsReplyUserdetail(newsreply, userdetail)
        userdetailnewsreplylist.append(temp)

    if request.session.has_key('username'):
        islog = 1
        username = request.session['username']
        account = Account.objects.get(username = username)
        context = {
        'newss': newss,
        'news': news,
        'islog': islog,
        'username': username,
        'account': account,
        'newsreplys': newsreplys,
        'lennewsrep': lennewsrep,
        'userdetailnewsreplylist': userdetailnewsreplylist,
        }
        return render(request, 'usernews/usernewsblog.html', context)

    context = {
        'newss': newss,
        'news': news,
        'islog': islog,
        'newsreplys': newsreplys,
        'lennewsrep': lennewsrep,
        'userdetailnewsreplylist': userdetailnewsreplylist,
    }
    return render(request, 'usernews/usernewsblog.html', context)

# def usernewspost(request):
#     islog = 0
#     if request.session.has_key('username'):
#         islog = 1
#         account = Account.objects.get(username = request.session['username'])
        
#         if account.accounttypeid.accounttypeid == 1:
#             enviromentcates = EnviromentCate.objects.all()
#             if request.method == "POST":
#                 enviromentcateid = request.POST.get('enviromentcateid')
#                 newsname = request.POST.get('newsname')
#                 content = request.POST.get('content')
#                 description = request.POST.get('description')
#                 try:
#                     avatar = request.FILES.get('avatar')
#                 except:
#                     avatar = None
#                 if avatar != None:
#                     ava = tokenFile(avatar)
#                 else:
#                     ava = ''
#                 note = request.POST.get('note')

#                 news = News(
#                     enviromentcateid = EnviromentCate.objects.get(enviromentcateid = enviromentcateid),
#                     accountid = account,
#                     newsname = newsname,
#                     description = description,
#                     content = content,
#                     createdate = datetime.now(),
#                     editdate = datetime.now(),
#                     avatar = ava,
#                     isenable = 1,
#                     note = note,
#                 )
#                 news.save()
#                 context = {
#                 'islog': islog,
#                 'account': account,
#                 'enviromentcates': enviromentcates,
#                 }
#                 return redirect('usernews:usernews')
#             else:
#                 context = {
#                     'islog': islog,
#                     'account':account,
#                     'enviromentcates': enviromentcates,
#                 }
#                 return render(request, 'usernews/usernewspost.html', context)       
#         else:
#             return redirect('homepage:index')

        
#     else:  
#         return redirect('homepage:index')

def myusernewspost(request, id):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()
        
        # header = Header.objects.get(headername = 'News')

        if request.method == "POST":
            if request.POST.get('enviromentcateid') == None or request.POST.get('enviromentcateid') == ' ':
                enviromentcateid = None
            else:
                enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST.get('enviromentcateid'))
            description = request.POST.get('description')

            newsname = request.POST.get('newsname')
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

            news = News(
                enviromentcateid = enviromentcateid,
                accountid = account,
                newsname = newsname,
                description = description,
                content = content,
                createdate = datetime.now(),
                editdate = datetime.now(),
                avatar = ava,
                isenable = 1,
                note = note,
            )
            news.save()
        
            return redirect('usernews:myusernews', account.accountid)

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            }
        return render(request, 'usernews/myusernewspost.html', context)
    else:  
        return redirect('homepage:index')

def myusernews(request, id):
    islog = 0
    enviromentcates = EnviromentCate.objects.all() 

    header = Header.objects.get(headername = 'News')   

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        newss = News.objects.filter(accountid = account.accountid).order_by('-createdate')

        userdetailnewslist = []
        for news in newss:
            # news.newsid = 'NewsDelete(' + str(news.newsid) + ')'
            userdetail =  UserDetail.objects.get(accountid = news.accountid)
            temp = NewsUserdetail(news, userdetail)
            userdetailnewslist.append(temp)

        # Quy định cách hiển thị table forum khi đã đăng nhập
        classdiv = "col-lg-9"

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'newss': newss,
            'userdetailnewslist': userdetailnewslist,
            'classdiv': classdiv,
            'header': header,
        }
        return render(request, 'usernews/myusernews.html', context)

    return redirect('homepage:index')

def myusernewsedit(request, idacc, idnew):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        news = News.objects.get(newsid = idnew)
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()
       
        if request.method == "POST":
            if request.POST.get('enviromentcateid') == None or request.POST.get('enviromentcateid') == ' ':
                enviromentcateid = None
            else:
                enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST.get('enviromentcateid'))
            newsname = request.POST.get('newsname')
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

            
            # if(enviromentcateid != forum.enviromentcateid.enviromentcateid):
            news = News.objects.filter(newsid = idnew).update(enviromentcateid = enviromentcateid)
            news = News.objects.filter(newsid = idnew).update(newsname = newsname)
            news = News.objects.filter(newsid = idnew).update(editdate = datetime.now())
            news = News.objects.filter(newsid = idnew).update(description = description)
            news = News.objects.filter(newsid = idnew).update(content = content)
            news = News.objects.filter(newsid = idnew).update(note = note)
            
            
            
            return redirect('usernews:myusernews', account.accountid)

        context = {
            'islog': islog,
            'account':account,
            'enviromentcates': enviromentcates,
            'news': news,
            }
        return render(request, 'usernews/myusernewsedit.html', context)
    else:  
        return redirect('homepage:index')