from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime

# Load dữ liệu theo tab All/Popular và Enviromentcate
def ajaxShowFor(request):
    check = request.GET.get('check', None)
    enviromentcate = request.GET.get('enviromentcate', None)
    forname = request.GET.get('forname', None)
    page = request.GET.get('page', None)

    if page =='' or page == None:
        page=0
    else:
        page = int(page)
    # page

    if check == '2':
        if enviromentcate == '':
            searchforums = Forum.objects.filter(subjectid = None).order_by('-viewcount')
        else:
            searchforums = Forum.objects.filter(subjectid = None).filter(enviromentcateid = enviromentcate).order_by('-viewcount')   
    else:
        if enviromentcate == '':
            searchforums = Forum.objects.filter(subjectid = None).order_by('-createdate')
        else:
            searchforums = Forum.objects.filter(subjectid = None).filter(enviromentcateid = enviromentcate).order_by('-createdate')
    
    if forname == None or forname == '':
        pass
    else:
        searchforums = searchforums.filter(forumtopicname__icontains = forname)
   
    userdetailforumlist = []
    btnmore = 1
    first = 4*page 
    last = (page+1)*4
    if len(searchforums)<last:
        last = len(searchforums)
        btnmore = 0
    if first >= len(searchforums):
        searchforums=[]
    else:
        searchforums=searchforums[first:last]
    
    s = ''
    for searchforum in searchforums:
        userdetail =  UserDetail.objects.get(accountid = searchforum.accountid)
        temp = ForumUserdetail(searchforum, userdetail)
        userdetailforumlist.append(temp)
    
    for userforlist in userdetailforumlist:
        linkforumblog = '/userforumblog/' + str(userforlist.forum.forumtopicid) + '/'
        if userforlist.forum.avatar != None:
            img = '<img src="'  + str(userforlist.forum.avatar) + '" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
        else:
            img = '<img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
	
        s += '<tr><td class="options" style="width:5%; text-align:center;"><div class="thumb_cart" style = "border-radius: 50%">'
        s += img + '</div></td>'
        s += '<td style="text-align: justify"><span class="options" ><a href="' + linkforumblog + '">' + str(userforlist.forum.forumtopicname) + '</a></span></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.userdetail.lastname) + ' ' + str(userforlist.userdetail.firstname) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.createdate.day) + '-' + str(userforlist.forum.createdate.month) + '-' + str(userforlist.forum.createdate.year) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.viewcount) + '</strong></td></tr>'

    data= {
        'btnmore':btnmore,
        'page':page,
        's': s
    }

    return JsonResponse(data)

# Load Bình Luận cho Forum (gồm xóa và tạo cmt)
def ajaxShowCommentFor(request):
    accountid = request.GET.get('accountid', None)
    forumtopicid = request.GET.get("forumtopicid", None)
    content = request.GET.get("content", None)
    forum = Forum.objects.get(forumtopicid =  forumtopicid)
    account = Account.objects.get(accountid = accountid)
    page = request.GET.get('page', None)
    delforcmt = request.GET.get('delforcmt', None)
    creforcmt = request.GET.get('creforcmt', None)

    if page == None or page == '':
        page = 0
    else:
        page = int(page)

    forumreplyid = request.GET.get("forumreplyid", None)

    if forumtopicid == None or forumtopicid == '':
        pass
    else:
        forumtopicid = int(forumtopicid)

    if forumreplyid == None or forumreplyid == '':
        pass
    else:
        forumreplyid = int(forumreplyid)

    if delforcmt == '1':
        # Lấy forumreply
        forumreply = ForumReply.objects.get(forumreplyid=forumreplyid)
        # Lấy forumtopicid
        forumtopicid =  forumreply.forumtopicid
        # Xóa forumreply
        forumreply.delete()

    if creforcmt == '1':
        forumreply = ForumReply(
            accountid = account,
            forumtopicid = forum,
            content = content,
            createdate = datetime.now(),
            editdate = datetime.now(),
            isenable = 1,
            note = '',
        )
        forumreply.save()
   
    
    # Load forumreplys
    forumreplys = ForumReply.objects.filter(forumtopicid= forumtopicid).order_by('-createdate')

    btnmore = 1
    first = 4*page
    last = (page+1)*4
    if len(forumreplys) < last:
        last = len(forumreplys)
        btnmore = 0
    if first >= len(forumreplys):
        forumreplys = []
    else:
        forumreplys = forumreplys[first:last]

    s = ''
    temp = ''
    for forumreply in forumreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        delbut=''
        if forumreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(forumreply.forumreplyid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        if forumreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(forumreply.accountid.avatar) + '" style="width:68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(forumreply.createdate.day) + '-' + str(forumreply.createdate.month) + '-' + str(forumreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(forumreply.content) + '</div></li>'
												
        s += temp
    data = {
        's': s,
        'btnmore': btnmore,
        'page':page,
    }
    return JsonResponse(data)

# Load dữ liệu theo tab All/Popular và Enviromentcate trong Myuserforum
def ajaxShowForOfMe(request):
    forname = request.GET.get('forname', None)
    check = request.GET.get('check', None)
    enviromentcate = request.GET.get('enviromentcate', None)
    username = request.session['username']
    account = Account.objects.get(username = username)
    page = request.GET.get('page', None)
    delfor = request.GET.get('delfor', None)
    forumtopicid = request.GET.get('forumtopicid', None)
    
    if forumtopicid == None or forumtopicid == '':
        pass
    else:
        forumtopicid = int(forumtopicid)
    
    if page == '' or page == None:
        page = 0
    else:
        page = int(page)

    if delfor == '1':
        forumreplys = ForumReply.objects.filter(forumtopicid = forumtopicid)
        for forumreply in forumreplys:
            forumreply.delete()
        
        forumlikes = ForumLike.objects.filter(forumtopicid = forumtopicid)
        for forumlike in forumlikes:
            forumlike.delete()
        
        forum = Forum.objects.get(forumtopicid = forumtopicid)
        forum.delete()

    if check == '2':
        if enviromentcate == '':
            searchforums = Forum.objects.filter(accountid = account.accountid).order_by('-viewcount')
        else:
            searchforums = Forum.objects.filter(accountid = account.accountid).filter(enviromentcateid = enviromentcate).order_by('-viewcount')
    else:
        if enviromentcate == '':
            searchforums = Forum.objects.filter(accountid = account.accountid).order_by('-createdate')
        else:
            searchforums = Forum.objects.filter(accountid = account.accountid).filter(enviromentcateid = enviromentcate).order_by('-createdate')
        
    if forname == None or forname == '':
        pass
    else:
        searchforums = searchforums.filter(forumtopicname__icontains = forname)

    btnmore = 1
    first = 9*page
    last = (page+1)*9
    if len(searchforums) < last:
        last = len(searchforums)
        btnmore = 0
    if first >= len(searchforums):
        searchforums = []
    else:
        searchforums = searchforums[first:last]

    userdetailforumlist = []
    s = ''
    for searchforum in searchforums:
        userdetail =  UserDetail.objects.get(accountid = searchforum.accountid)
        temp = ForumUserdetail(searchforum, userdetail)
        userdetailforumlist.append(temp)
    
    for userforlist in userdetailforumlist:
        linkforumblog = '/userforumblog/' + str(userforlist.forum.forumtopicid) + '/'
        delbut = '<td><button  onclick=ForumDelete(' + str(userforlist.forum.forumtopicid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button></td>'
        if userforlist.forum.avatar != None:
            img = '<img src="'  + str(userforlist.forum.avatar) + '" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
        else:
            img = '<img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
		
        s += '<tr><td class="options" style="width:5%; text-align:center;"><div class="thumb_cart" style = "border-radius: 50%">'
        s += img + '</div></td>'
        s += '<td style="text-align: justify"><span class="options" ><a href="' + linkforumblog + '">' + str(userforlist.forum.forumtopicname) + '</a></span></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.userdetail.lastname) + ' ' + str(userforlist.userdetail.firstname) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.createdate.day) + '-' + str(userforlist.forum.createdate.month) + '-' + str(userforlist.forum.createdate.year) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.viewcount) + '</strong></td>' 
        s += '<td class="options" style="width:5%; text-align:center;"><a href="' + '/myuserforumedit/' + str(account.accountid) + '/forum/' + str(userforlist.forum.forumtopicid) + '/' + '"><i class="icon-edit"></i>Sửa</a></td>'
        s += delbut
        s += '</tr>'

    data= {
        'btnmore': btnmore,
        'page':page,
        's': s,
    }

    return JsonResponse(data)

def ajaxLikeFor(request):
    forid = request.GET.get("forid", None)
    forum = Forum.objects.get(forumtopicid = forid)
    
    username = request.session['username']
    account = Account.objects.get(username=username)
        
    forumlike = ForumLike(
                                accountid = Account.objects.get(accountid = account.accountid),
                                forumtopicid = forum,
                                status = 1,
                                isenable = 1,
        )
    forumlike.save()

    forlikes = ForumLike.objects.filter(forumtopicid = forid)
    likecount = len(forlikes)
    data = {
        'likecount': ' ' + str(likecount)
    }

    return JsonResponse(data)

def ajaxUnLikeFor(request):
    forid = request.GET.get("forid", None)
    username = request.session["username"]
    acc = Account.objects.get(username=username)
    forlike =  ForumLike.objects.filter(accountid=acc.accountid).filter(forumtopicid = forid)
    forlike.delete()
    forlikes = ForumLike.objects.filter(forumtopicid = forid)
    likecount = len(forlikes)
    data = {
        'likecount': ' ' + str(likecount)
    }
    return JsonResponse(data)

def chatsent(request):
    content = request.GET.get('content')
    username = request.session["username"]
    acc = Account.objects.get(username=username)
    fastchatnew = FastChat(
        accountid=acc,
        content=content,
        createdate=datetime.now(),
        isenable=1,
        note=''
    )
    fastchatnew.save()
    data={
        's':True
    }
    return JsonResponse(data)

def requestchat(request):
    lastid = request.GET.get('lastid', None)
    lastid=int(lastid)+1
    fastchats = FastChat.objects.filter(fastchatid__gte=lastid)
    s=''
    try:
        account = Account.objects.get(username=request.session['username'])
        log = 1
    except:
        log= 0
    
    if log ==1:
        for fastchat in fastchats :
            if fastchat.accountid.accountid==account.accountid:
                temp=''' <div align="right" style="padding-top:15px; padding-bottom:15px">
									
										<p style="display: inline;background-color:#ededed;border-radius:5%;color: black; padding-left: 10px;padding-right: 10px; font-size: 12pt">
										<strong>'''+fastchat.accountid.username+''' :</strong>'''+ fastchat.content+ '''
										</p>
										<img src="''' + fastchat.accountid.avatar+ '''" style="width:50px;height: 50px; border-radius: 50%;">
									</div>'''
            else:
                temp='''	<div align="left" style="padding-top:15px; padding-bottom:15px">
										<img src="''' + fastchat.accountid.avatar+ '''" style="width:50px;height: 50px; border-radius: 50%;">
										<p style="display: inline;background-color:white;border-radius:5%;color: black; padding-left: 10px;padding-right: 10px; font-size: 12pt">
										<strong>'''+fastchat.accountid.username+''' :</strong>'''+ fastchat.content+ '''
										</p>
									</div>'''
            s+=temp
    else:
        for fastchat in fastchats :
            temp='''	<div align="left" style="padding-top:15px; padding-bottom:15px">
										<img src="''' + fastchat.accountid.avatar+ '''" style="width:50px;height: 50px; border-radius: 50%;">
										<p style="display: inline;background-color:white;border-radius:5%;color: black; padding-left: 10px;padding-right: 10px; font-size: 12pt">
										<strong>'''+fastchat.accountid.username+''' :</strong>'''+ fastchat.content+ '''
										</p>
									</div>'''
            s+=temp
    if len(fastchats)> 0:
        newlastid = fastchats[len(fastchats)-1].fastchatid
    else:
        newlastid = lastid-1
    data={
        's':s,
        'newlastid':newlastid
    }
    return JsonResponse(data)