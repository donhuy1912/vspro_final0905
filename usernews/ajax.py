from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator

def ajaxSearchNew(request):
    newsname = request.GET.get('newsname', None)
    page = request.GET.get('page', None)
    if page == '' or page == None:
        page = 0
    else:
        page = int(page)

    if newsname == None or newsname == '':
        searchnewss = News.objects.all().order_by('-createdate')
    else:
        searchnewss = News.objects.filter(newsname__icontains = newsname).order_by('-createdate') # icontains: tìm kiếm gần đúng
    
    btnmore = 1
    first = 4*page
    last = (page+1)*4
    if len(searchnewss)<last:
        last = len(searchnewss)
        btnmore = 0
    if first >= len(searchnewss):
        searchnewss = []
    else:
        searchnewss = searchnewss[first:last]

    s = ''
    userdetailnewslist = []
    for searchnews in searchnewss:
        userdetail =  UserDetail.objects.get(accountid = searchnews.accountid)
        temp = NewsUserdetail(searchnews, userdetail)
        userdetailnewslist.append(temp)

    for usernewslist in userdetailnewslist:
        linknewsblog = '/usernewsblog/' + str(usernewslist.news.newsid) + '/'
        if usernewslist.news.avatar != None:
            img = '<figure><img style ="width: 250px; height: 205.156px" src="'  + str(usernewslist.news.avatar) + '" alt="">'
        else:
            img = '<figure><img src="http://via.placeholder.com/500x333/ccc/fff/news_home_1.jpg" alt="">'
		
        s += '<div class="col-lg-6">'
        s += '<a class="box_news" href="' + linknewsblog + '">'
        s += img
        s += '<figcaption><strong>' + str(usernewslist.news.createdate.day) + '</strong>' + str(usernewslist.news.createdate.month) + '</figcaption>'
        s += '</figure>'
        s += '<ul>'
        s += '<li>' + str(usernewslist.userdetail.lastname) + ' ' + str(usernewslist.userdetail.firstname) + '</li>'
        s += '<li>' + str(usernewslist.news.createdate.day) + '.' + str(usernewslist.news.createdate.month) + '.' + str(usernewslist.news.createdate.year) + '</li>'
        s += '</ul>'
        s += '<h4 style="text-align: justify">' + str(usernewslist.news.newsname) + '</h4>'
        s += '<p style="text-align: justify">' + str(usernewslist.news.description) + '</p>'
        s += '</a>'
        s += '</div>'
    data= {
        'btnmore': btnmore,
        'page':page,
        's': s,
    }

    return JsonResponse(data)

# Xóa NewsReply
def ajaxDelCommentNew(request):
    newsreplyid = request.GET.get("newsreplyid", None)
    # Lấy newsreply
    newsreply = NewsReply.objects.get(newsreplyid=newsreplyid)
    # Lấy newsid
    newsid =  newsreply.newsid
    # Xóa newsreply
    newsreply.delete()
    # Load newsreply
    newsreplys = NewsReply.objects.filter(newsid= newsid).order_by('-createdate')
    s = ''
    temp = ''
    for newsreply in newsreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = newsreply.accountid)
        delbut=''
        if newsreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(newsreply.newsreplyid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        if newsreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(newsreply.accountid.avatar) + '" style="width: 68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(newsreply.createdate.day) + '-' +str(newsreply.createdate.month) + '-' + str(newsreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(newsreply.content) + '</div></li><br>'
												
        s += temp
    data = {
        's': s
    }
    return JsonResponse(data)

# Tạo NewsReply
def ajaxCreateCommentNew(request):
    accountid = request.GET.get('accountid', None)
    newsid = request.GET.get("newsid", None)
    content = request.GET.get("content", None)
    news = News.objects.get(newsid =  newsid)
    

    account = Account.objects.get(accountid = accountid)
    
    
    newsreply = NewsReply(
        accountid = account,
        newsid = news,
        content = content,
        createdate = datetime.now(),
        editdate = datetime.now(),
        isenable = 1,
        note = '',
    )
    newsreply.save()
    
    # Load newsreplys
    newsreplys = NewsReply.objects.filter(newsid= newsid).order_by('-createdate')
    s = ''
    temp = ''
    for newsreply in newsreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = newsreply.accountid)
        delbut=''
        if newsreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(newsreply.newsreplyid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        if newsreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(newsreply.accountid.avatar) + '" style="width: 68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(newsreply.createdate.day) + '-' +str(newsreply.createdate.month) + '-' + str(newsreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(newsreply.content) + '</div></li><br>'
												
        s += temp
    data = {
        's': s
    }
    return JsonResponse(data)

# Load Bình Luận cho News (gồm xóa và tạo cmt)
def ajaxShowCommentNews(request):
    accountid = request.GET.get('accountid', None)
    newsid = request.GET.get("newsid", None)
    content = request.GET.get("content", None)
    news = News.objects.get(newsid =  newsid)
    account = Account.objects.get(accountid = accountid)
    page = request.GET.get('page', None)
    delnewscmt = request.GET.get('delnewscmt', None)
    crenewscmt = request.GET.get('crenewscmt', None)

    if page == None or page == '':
        page = 0
    else:
        page = int(page)

    newsreplyid = request.GET.get("newsreplyid", None)

    if newsid == None or newsid == '':
        pass
    else:
        newsid = int(newsid)

    if newsreplyid == None or newsreplyid == '':
        pass
    else:
        newsreplyid = int(newsreplyid)

    print('newsid: ', newsid)
    print('newsreplyid: ', newsreplyid)
    print('news: ', news)
    print('delnewscmt', delnewscmt)
    print('crenewscmt', crenewscmt)
    print('content', content)

    if delnewscmt == '1':
        # Lấy newsreply
        newsreply = NewsReply.objects.get(newsreplyid=newsreplyid)
        # Lấy newsid
        newsid =  newsreply.newsid
        # Xóa newsreply
        newsreply.delete()

    if crenewscmt == '1':
        newsreply = NewsReply(
            accountid = account,
            newsid = news,
            content = content,
            createdate = datetime.now(),
            editdate = datetime.now(),
            isenable = 1,
            note = '',
        )
        newsreply.save()
   
    
    # Load newsreplys
    newsreplys = NewsReply.objects.filter(newsid= newsid).order_by('-createdate')

    btnmore = 1
    first = 4*page
    last = (page+1)*4
    if len(newsreplys) < last:
        last = len(newsreplys)
        btnmore = 0
    if first >= len(newsreplys):
        newsreplys = []
    else:
        newsreplys = newsreplys[first:last]

    s = ''
    temp = ''
    for newsreply in newsreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = newsreply.accountid)
        delbut=''
        if newsreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(newsreply.newsreplyid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        if newsreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(newsreply.accountid.avatar) + '" style="width: 68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(newsreply.createdate.day) + '-' +str(newsreply.createdate.month) + '-' + str(newsreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(newsreply.content) + '</div></li><br>'
												
        s += temp
    data = {
        's': s,
        'btnmore': btnmore,
        'page':page,
    }
    return JsonResponse(data)

# Thiết đặt sự kiện cho thanh Tìm kiếm trong Myusernews
def ajaxSearchNewsOfMe(request):
    page = request.GET.get('page', None)
    delnews = request.GET.get('delnews', None)
    newsid = request.GET.get('newsid', None)
    newsname = request.GET.get('newsname', None)
    username = request.session['username']
    account = Account.objects.get(username = username)

    if newsid == None or newsid == '':
        pass
    else:
        newsid = int(newsid)
    
    if page == '' or page == None:
        page = 0
    else:
        page = int(page)

    if delnews == '1':
        newsreplys = NewsReply.objects.filter(newsid = newsid)
        for newsreply in newsreplys:
            newsreply.delete()
        
        news = News.objects.get(newsid = newsid)
        news.delete()

    if newsname == None or newsname == '':
        searchnewss = News.objects.filter(accountid = account.accountid).order_by('-createdate')
    else:
        searchnewss = News.objects.filter(accountid = account.accountid).filter(newsname__icontains = newsname).order_by('-createdate') # icontains: tìm kiếm gần đúng
    
    btnmore = 1
    first = 4*page 
    last = (page+1)*4
    if len(searchnewss)<last:
        last = len(searchnewss)
        btnmore = 0
    if first >= len(searchnewss):
        searchnewss=[]
    else:
        searchnewss=searchnewss[first:last]


    s = ''
    userdetailnewslist = []
    for searchnews in searchnewss:
        userdetail =  UserDetail.objects.get(accountid = searchnews.accountid)
        temp = NewsUserdetail(searchnews, userdetail)
        userdetailnewslist.append(temp)
    									
    for usernewslist in userdetailnewslist:
        linknewsblog = '/usernewsblog/' + str(usernewslist.news.newsid) + '/'
        # delbut='<td class="options" style="width:5%; text-align:center;"><a onclick= NewsDelete(' + str(usernewslist.news.newsid) + ')><i class="icon-edit"></i>Xóa</a></td>'
        delbut = '<td><button  onclick=NewsDelete(' + str(usernewslist.news.newsid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button></td>'
        if usernewslist.news.avatar != None:
            img = '<img src="'  + str(usernewslist.news.avatar) + '" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
        else:
            img = '<img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
		
        s += '<tr><td class="options" style="width:5%; text-align:center;"><div class="thumb_cart" style = "border-radius: 50%">'
        s += img + '</div></td>'
        s += '<td style="text-align: justify"><span class="options" ><a href="' + linknewsblog + '">' + str(usernewslist.news.newsname) + '</a></span></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(usernewslist.userdetail.lastname) + ' ' + str(usernewslist.userdetail.firstname) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(usernewslist.news.createdate.day) + '-' + str(usernewslist.news.createdate.month) + '-' + str(usernewslist.news.createdate.year) + '</strong></td>'
        # s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(usernewslist.news.viewcount) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><a href="' + '/myusernewsedit/' + str(account.accountid) + '/news/' + str(usernewslist.news.newsid) + '/' +'"><i class="icon-edit"></i>Sửa</a></td>'
        s += delbut
        s += '</tr>'

    data= {
       's': s,
       'btnmore': btnmore,
       'page':page,
    }

    return JsonResponse(data)
