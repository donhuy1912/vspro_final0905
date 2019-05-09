from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from homepage.stringprocess import *
from random import randint


def ajaxsentmes(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        content=request.GET.get('content')
        try:
            chatrooms=ChatRoom.objects.get(accountid=account)
        except:
            chatroomnew=ChatRoom(
                supportid=None,
                accountid=account,
                createdate =  datetime.now(),
            )
            chatroomnew.save()
            chatrooms=ChatRoom.objects.get(accountid=account)
        chat=Chat(
            chatroomid=chatrooms,
            accountid=account,
            createdate =  datetime.now(),
            content=content
        )
        chatrooms.createdate=datetime.now()
        chatrooms.save()
        chat.save()
        data = {
            's':True
        }
        return JsonResponse(data)
    else:
        content=request.GET.get('content')
        ipcom = request.GET.get('userip')
        sip = ''
        for ip in ipcom:
            if ip != '.':
                sip += ip
        
        usernameguest = 'vsguestid' + str(sip)
        # thêm acc
        try:
            acc = Account.objects.get(username=usernameguest)
            ipacc = getNumInString(usernameguest)
            if int(sip) != ipacc:
                accnew = Account(
                    accounttypeid = AccountType.objects.get(accounttypeid =  3),
                    username = usernameguest,
                    password = hashPassword(usernameguest), 
                    createdate =  datetime.now(), 
                    editdate =  datetime.now(),
                    avatar = '/media/userava.png',
                    isenable = 1,
                    note = '',
                )
                accnew.save()
                userdetailnew = UserDetail(
                    accountid = Account.objects.get(accountid = accnew.accountid),
                    firstname = 'guest', 
                    lastname = 'vspro', 
                    phonenumber = str(sip), 
                    email = usernameguest + '@gmail.com'
                )
                userdetailnew.save()
        except:
            accnew = Account(
                accounttypeid = AccountType.objects.get(accounttypeid =  3),
                username = usernameguest,
                password = hashPassword(usernameguest), 
                createdate =  datetime.now(), 
                editdate =  datetime.now(),
                avatar = '/media/userava.png',
                isenable = 1,
                note = '',
            )
            accnew.save()
            userdetailnew = UserDetail(
                accountid = Account.objects.get(accountid = accnew.accountid),
                firstname = 'guest', 
                lastname = 'vspro', 
                phonenumber = str(sip), 
                isenable = 1,
                email = usernameguest + '@gmail.com'
            )
            userdetailnew.save()

        account = Account.objects.get(username=usernameguest)
        # content
        try:
            chatrooms=ChatRoom.objects.get(accountid=account)
        except:
            chatroomnew=ChatRoom(
                supportid=None,
                accountid=account,
                createdate =  datetime.now(),
            )
            chatroomnew.save()
            chatrooms=ChatRoom.objects.get(accountid=account)

        chat=Chat(
            chatroomid=chatrooms,
            accountid=account,
            createdate = datetime.now(),
            content=content
            )
        chatrooms.createdate=datetime.now()
        chatrooms.save()
        chat.save()

        data={
            's': 0
        }
        return JsonResponse(data)

def getallmes(request):
    s=''
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        try:
            chatrooms=ChatRoom.objects.get(accountid=account)
        except:
            chatroomnew=ChatRoom(
                supportid=None,
                accountid=account,
                createdate =  datetime.now(),
            )
            chatroomnew.save()
            chatrooms=ChatRoom.objects.get(accountid=account)
        
        time_threshold = datetime.now() - timedelta(hours=5)
        chats=Chat.objects.filter(chatroomid=chatrooms).filter(createdate__gte=time_threshold).order_by('chatid')
       
        for chat in chats:
            
            temp='''<div class="chat-message clearfix">
					
					<img src=''' + chat.accountid.avatar +''' alt="" width="32" height="32">

					<div class="chat-message-content clearfix">
						
						<span class="chat-time">'''+ str(chat.createdate.hour) + ''':''' + str(chat.createdate.minute)  +'''</span>
                        <strong>'''+chat.accountid.username+'''</strong>
						<p> '''+ chat.content +''' </p>

					</div> 
					<hr>
				</div>'''
            s=s+temp
        if len(chats) > 0:
            lastid= chats[len(chats)-1].chatid 
        else: 
            lastid=0
        
        data={
            'flag':True,
            'lastid':lastid,
            's':s
        }
        return JsonResponse(data)
    else: 
        ipcom = request.GET.get('userip')
        sip = ''
        for ip in ipcom:
            if ip != '.':
                sip += ip
            
        usernameguest = 'vsguestid' + str(sip)
        account = Account.objects.get(username=usernameguest)
        
        try:
            chatrooms=ChatRoom.objects.get(accountid=account)
        except:
            chatroomnew=ChatRoom(
                supportid=None,
                accountid=account,
                createdate = datetime.now(),
            )
            chatroomnew.save()
            chatrooms=ChatRoom.objects.get(accountid=account)
        
        time_threshold = datetime.now() - timedelta(hours=5)
        chats=Chat.objects.filter(chatroomid=chatrooms).filter(createdate__gte=time_threshold).order_by('chatid')
       
        for chat in chats:
            
            temp='''<div class="chat-message clearfix">
					
					<img src=''' + chat.accountid.avatar +''' alt="" width="32" height="32">

					<div class="chat-message-content clearfix">
						
						<span class="chat-time">'''+ str(chat.createdate.hour) + ''':''' + str(chat.createdate.minute)  +'''</span>
                        <strong>'''+chat.accountid.username+ '''</strong>
						<p> '''+ chat.content +''' </p>

					</div> 
					<hr>
				</div>'''
            s=s+temp
        if len(chats) > 0:
            lastid= chats[len(chats)-1].chatid 
        else: 
            lastid=0
        
        data={
            'flag':True,
            'lastid':lastid,
            's':s
        }
        return JsonResponse(data)

def getmes(request):
    try:
        lastidold=int(request.GET.get('lastid'))
    except:
        lastidold=0
    
    s=''
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        chatrooms=ChatRoom.objects.get(accountid=account)
        time_threshold = datetime.now() - timedelta(hours=5)
        chats=Chat.objects.filter(chatroomid=chatrooms).filter(createdate__gte=time_threshold).filter(chatid__gt=lastidold).order_by('chatid')
        alllchat=Chat.objects.filter(chatroomid=chatrooms).order_by('chatid')
        
        
        for chat in chats:
            temp='''<div class="chat-message clearfix">
					
					<img src=''' + chat.accountid.avatar +''' alt="" width="32" height="32">

					<div class="chat-message-content clearfix">
		
						<span class="chat-time">'''+ str(chat.createdate.hour) + ''':''' + str(chat.createdate.minute)  +'''</span>
                        <strong>'''+chat.accountid.username+'''</strong>
						<p> '''+ chat.content +''' </p>

					</div> 
					<hr>
				</div>'''
            s=s+temp
        if len(alllchat) > 0:
            lastid= alllchat[len(alllchat)-1].chatid
 
        else: 
            lastid=0
        
        count=lastid-lastidold
        data={
            'count':count,
            'lastid':lastid,
            'flag':True,
            's':s
        }
        return JsonResponse(data)
    else:
        s=''
        try:
            ipcom = request.GET.get('userip')
            sip = ''
            for ip in ipcom:
                if ip != '.':
                    sip += ip
            
            usernameguest = 'vsguestid' + str(sip)
            account = Account.objects.get(username=usernameguest)

            chatrooms=ChatRoom.objects.get(accountid=account)
            time_threshold = datetime.now() - timedelta(hours=5)
            chats=Chat.objects.filter(chatroomid=chatrooms).filter(createdate__gte=time_threshold).filter(chatid__gt=lastidold).order_by('chatid')
            alllchat=Chat.objects.filter(chatroomid=chatrooms).order_by('chatid')
            
            
            for chat in chats:
                temp='''<div class="chat-message clearfix">
                        
                        <img src=''' + chat.accountid.avatar +''' alt="" width="32" height="32">

                        <div class="chat-message-content clearfix">
            
                            <span class="chat-time">'''+ str(chat.createdate.hour) + ''':''' + str(chat.createdate.minute)  +'''</span>
                            <strong>'''+chat.accountid.username+'''</strong>
                            <p> '''+ chat.content +''' </p>

                        </div> 
                        <hr>
                    </div>'''
                

                s=s+temp
               
            if len(alllchat) > 0:
                lastid= alllchat[len(alllchat)-1].chatid
            else: 
                lastid=0
            
            count=lastid-lastidold
            data={
                'count':count,
                'lastid':lastid,
                'flag':True,
                's':s
            }
            return JsonResponse(data)
        except:
            data={
                    'flag':False,
                    's':s,
                }
            
            return JsonResponse(data)
#admin chat
def getallroomchat(request):
    searoom=request.GET.get('searoom')
    if searoom != '':
        
        accounts = Account.objects.filter(username__icontains=searoom)
        arracc=[]
        for account in accounts:
            arracc.append(account.accountid)
        chatrooms=ChatRoom.objects.filter(accountid__in=arracc).order_by('-createdate')
        
    if searoom == '':
        chatrooms=ChatRoom.objects.order_by('-createdate')
    
    s=''
    for chatroom in chatrooms:
        try:
            chat=Chat.objects.filter(chatroomid=chatroom.chatroomid).order_by("-chatid")[0]
            chatcontent = chat.content[0:40]
        except:
            chatcontent = 'Không có tin nhắn'
        temp=''' <a id='chatroomlist' href="#"  onclick="changeroom('''+ str(chatroom.chatroomid) +''')">
                                <div class="mail_list">
                                  <div class="left">
                                   
                                  </div>
                                  <div class="right">
                                    <h3 style="color:green">'''+ str(chatroom.accountid.username) +''' <small>'''+ str(chatroom.createdate.hour) + ''':''' + str(chatroom.createdate.minute)  +'''</small></h3>
                                    <p>'''+ chatcontent +'''</p>
                                  </div>
                                </div>
                              </a>'''
        s=s+temp
    data={
        's':s
    }
    return JsonResponse(data)

def getallmesadmin(request):
    idroom=int(request.GET.get('idroom'))
    s=''
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])

        chatrooms=ChatRoom.objects.get(chatroomid=idroom)
        chats=Chat.objects.filter(chatroomid=chatrooms).order_by('createdate')
        
        for chat in chats:
            temp='''<div class="sender-info">
                            <div class="row">
                              <div class="col-md-12">
                                <strong style='color:green'>''' + chat.accountid.username+ '''</strong>
                                
                                
                              </div>
                            </div>
                          </div>
                          <div class="view-mail">
                            <p>'''+ chat.content +''' </p>
                              <hr>
                                                          
                          </div>'''
            s=s+temp
        if len(chats) > 0:
            lastid= chats[len(chats)-1].chatid 
        else: 
            lastid=0
        data={

            'flag':True,
            'lastid':lastid,
            's':s
        }
        return JsonResponse(data)
    else:
        data={
            'flag':False,
            's':s
        }
        return JsonResponse(data)

def getmesadmin(request):
    idroom=int(request.GET.get('idroom'))
    try:
        lastidold=int(request.GET.get('lastid'))
    except:
        lastidold=0
    
    s=''
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        chatrooms=ChatRoom.objects.get(chatroomid=idroom)

        chats=Chat.objects.filter(chatroomid=chatrooms).filter(chatid__gt=lastidold).order_by('chatid')
        alllchat=Chat.objects.filter(chatroomid=chatrooms).order_by('chatid')
        for chat in chats:
            temp='''<div class="sender-info">
                            <div class="row">
                              <div class="col-md-12">
                                <strong style='color:green'>''' + chat.accountid.username+ '''</strong>
                                
                                
                              </div>
                            </div>
                          </div>
                          <div class="view-mail">
                            <p>'''+ chat.content +''' </p>
                              <hr>
                                                          
                          </div>'''
            s=s+temp
        if len(alllchat) > 0:
            lastid= alllchat[len(alllchat)-1].chatid
        else: 
            lastid=0
        
        count=lastid-lastidold
        data={
            'count':count,
            'lastid':lastid,
            'flag':True,
            's':s
        }
        return JsonResponse(data)
    else:
        data={
            'flag':False,
            's':s
        }
        return JsonResponse(data)

def sentmesadmin(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        content=request.GET.get('content')
        idroom=int(request.GET.get('idroom'))
        
        chatrooms=ChatRoom.objects.get(chatroomid=idroom)
        
        chat=Chat(
            chatroomid=chatrooms,
            accountid=account,
            createdate =  datetime.now(),
            content=content
        )
        chatrooms.createdate=datetime.now()
        chatrooms.save()
        chat.save()
        data={
            's':True
        }
        return JsonResponse(data)
    else:
        data={
            's':False
        }
        return JsonResponse(data)

def logingmail(request):
    gid=request.GET.get('id')
    name=request.GET.get('name')
    ava=request.GET.get('ava')
    email=request.GET.get('email') 

    kdname=no_accent_vietnamese(name)
    splitname=name.split(' ')
    num = len(splitname)
    firstname=splitname[0]
    lastname=splitname[num-1]
    accounts = Account.objects.all()
    try:
        usercheck=UserDetail.objects.get(email=email)
        accountgmail=usercheck.accountid
    except:
        while True:
            usernamenew=no_accent_vietnamese(lastname+firstname)+str(randint(0,9999))
            try:
                account=Account.objects.get(username=usernamenew)
            except:
                break
       
        accountnew=Account(
            accounttypeid = AccountType.objects.get(accounttypeid = 3),
            username = usernamenew,
            password = hashPassword('asdasdasd'), 
            createdate =  datetime.now(), 
            editdate =  datetime.now(),
            avatar = ava,
            resetcode = '',
            isenable = 1,  
        )            
        accountnew.save()
        usedetailnew = UserDetail(
            accountid = Account.objects.get(username=usernamenew),
            firstname = firstname, 
            lastname = lastname, 
            birthday =  datetime.now(),
            address = ' ', 
            phonenumber = None, 
            email = email, 
            isenable = 1,
        )
        usedetailnew.save()
        usercheck=UserDetail.objects.get(email=email)
        accountgmail=usercheck.accountid
    request.session['username'] = accountgmail.username
    data={
        
    }
    return JsonResponse(data)


def loginfacebook(request):
    id = request.GET.get('id')
    name = request.GET.get('name')
    avatar = 'http://graph.facebook.com/' + str(id) + '/picture'
    
    kdname=no_accent_vietnamese(name)
    splitname=name.split(' ')
    num = len(splitname)
    fname = splitname[0]
    lname = splitname[num-1]
    # email
    email = 'www.facebook.com/profile.php?id=' + str(id)
    accounts = Account.objects.all()
    try:
        usercheck=UserDetail.objects.get(email=email)
        accountgmail=usercheck.accountid
    except:
        while True:
            usernamenew=no_accent_vietnamese(lname+fname)+str(randint(0,9999))
            try:
                account=Account.objects.get(username=usernamenew)
            except:
                break
       
        accountnew=Account(
            accounttypeid = AccountType.objects.get(accounttypeid = 3),
            username = usernamenew,
            password = hashPassword('asdasdasd'), 
            createdate =  datetime.now(), 
            editdate =  datetime.now(),
            avatar = avatar,
            resetcode = '',
            isenable = 1,  
        )            
        accountnew.save()
        usedetailnew = UserDetail(
            accountid = Account.objects.get(username=usernamenew),
            firstname = fname, 
            lastname = lname, 
            birthday =  datetime.now(),
            address = ' ', 
            phonenumber = None, 
            email = email, 
            isenable = 1,
        )
        usedetailnew.save()
        usercheck=UserDetail.objects.get(email=email)
        accountgmail=usercheck.accountid
    request.session['username'] = accountgmail.username
    
    data = {

    }
    return JsonResponse(data)


def getroombutton(request):
    # getroombutton
    idroom = request.GET.get('idroom')
    idroom = int(idroom)

    if idroom != 0:
        butt = '''<button onclick="openpop(''' + str(idroom) + ''')"    class="btn btn-sm btn-primary" style="background-color:#cc0000;border-color:#cc0000" type="button"><i class="fa fa-trash"></i> Delete</button>'''
    else:
        butt = '''<button onclick="openpop(''' + str(idroom) + ''')"   class="btn btn-sm btn-primary" style="background-color:#ccccb3;border-color:#ccccb3" type="button" disabled><i class="fa fa-trash"></i> Delete</button>'''

    data = {
        'butt':butt
    }
    return JsonResponse(data)

def delmesadmin(request):
    idroom = request.GET.get('idroom')
    idroom = int(idroom)
    if request.session.has_key('username'):
        accountAdmin = Account.objects.get(username = request.session['username'])
        if accountAdmin.accounttypeid.accounttypeid == 1:
            chatroom = ChatRoom.objects.get(chatroomid = idroom)
            chats = Chat.objects.filter(chatroomid = chatroom.chatroomid)
            if (len(chats) > 0):
                for chat in chats:
                    chat.delete()
    data = {

    }
    return JsonResponse(data)


