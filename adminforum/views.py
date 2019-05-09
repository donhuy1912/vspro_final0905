from django.shortcuts import render, redirect
from homepage.models import Forum, EnviromentCate, Account, Subject,UserDetail
from datetime import datetime
from django.http import JsonResponse
from homepage.myfunction import tokenFile
# Create your views here.
def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forums = Forum.objects.all()
            for forum in forums:
                forum.createdate = forum.createdate
                forum.editdate = forum.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'forums': forums}
            return render(request, 'adminforum/forum_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                # Lấy url của avatar
                try:
                    token_avatar = request.FILES['avatar']
                except:
                    token_avatar = None
                ava = ''
                if token_avatar != None:
                    ava = tokenFile(token_avatar)

                if(request.POST.get('subjectid')=='0'):
                    subjectid = None
                else:
                    subjectid = Subject.objects.get(subjectid = request.POST.get('subjectid'))
                forum = Forum( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid']),
                                        subjectid = subjectid,
                                        forumtopicname = request.POST['forumname'],
                                        description = request.POST['description'],
                                        createdate = datetime.now(), 
                                        editdate = datetime.now(),
                                        content = request.POST['content'],
                                        viewcount = request.POST['viewcount'],  
                                        likecount = request.POST['likecount'],
                                        avatar = ava,  
                                        isenable = request.POST['isenable'],  
                                        note = request.POST['note'])
                forum.save()
                return redirect('/adminforum/')
            else:
                # subjectparts = SubjectPart.objects.all()
                # for subjectpart in subjectparts:
                #     subjectpart.createdate = subjectpart.createdate
                #     subjectpart.editdate = subjectpart.editdate

                enviromentcates = EnviromentCate.objects.all()
                for enviromentcate in enviromentcates:
                    enviromentcate.createdate = enviromentcate.createdate
                    enviromentcate.editdate = enviromentcate.editdate

                accounts = Account.objects.all()
                subjects = Subject.objects.all()
                
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate

                for subject in subjects:
                    subject.createdate = subject.createdate
                    subject.editdate = subject.editdate

                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts,
                    'subjects': subjects,
                    # 'subjectparts': subjectparts,
                    'enviromentcates': enviromentcates,
                }
            
            return render(request, 'adminforum/forum_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forum = Forum.objects.get(forumtopicid=id)
            forum.createdate = forum.createdate
            forum.editdate = datetime.now()

            enviromentcates = EnviromentCate.objects.all()
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = enviromentcate.editdate   

            accounts = Account.objects.all()
            subjects = Subject.objects.all()
                
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'forum': forum,
                # 'subjectparts': subjectparts,
                'accounts': accounts,
                'subjects': subjects,
                'enviromentcates': enviromentcates,
            } 
        
            return render(request, 'adminforum/forum_edit.html', context)
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
            forum = Forum.objects.filter(forumtopicid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            
            if request.POST.get('enviromentcateid')!= '0':
                forum = Forum.objects.filter(forumtopicid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNum(request.POST['enviromentcateid'])))
            forum = Forum.objects.get(forumtopicid=id)

            # Lấy url của avatar
            try:
                token_avatar = request.FILES['avatar']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = forum.avatar

            if request.POST.get('subjectid')  == '0':
                forum.subjectid=None
                
            forum.forumtopicname=request.POST['forumname']
            forum.description = request.POST['description']
            forum.createdate=forum.createdate
            forum.editdate=datetime.now()
            forum.content=request.POST['content']
            forum.viewcount=request.POST['viewcount']
            forum.likecount=request.POST['likecount']
            forum.avatar=ava
            forum.isenable=request.POST['isenable']
            forum.note=request.POST['note']
            forum.save()
            return redirect('/adminforum/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')



def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            forum = Forum.objects.get(forumtopicid= id)
            forum.delete()
            return redirect('/adminforum/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của subjectpart
def validate_enviromentcateforum(request):
    enviromentcate = request.GET.get('enviromentcate', None)
    subjects = Subject.objects.filter(enviromentcateid=enviromentcate)
    forum = Forum.objects.get(forumtopicid = request.GET.get('forum', None))
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
        
    if edit == True:
        forum  = Forum.objects.get(forumtopicid = request.GET.get('forum', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="subjectid" value="">-- Chọn --</option>'
        s += '<option type="text" name="subjectid" value="0">Chung</option>'
    else:
        if change == False:
            s= ' <option type="text" name="subjectid" value="' + str(forum.subjectid.subjectid) + ' ">' + forum.subjectid.subjectname + '</option>'
            s += '<option type="text" name="subjectid" value="0">Chung</option>'
    temp = ''

    for subject in subjects: 
        if edit == True and change == False:
            if subject.subjectid != forum.subjectid.subjectid:
                    temp = ' <option type="text" name="subjectid" value="' + str(subject.subjectid) + ' ">' + subject.subjectname + '</option>'
        else:
            temp = ' <option type="text" name="subjectid" value="' + str(subject.subjectid) + ' ">' + subject.subjectname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)