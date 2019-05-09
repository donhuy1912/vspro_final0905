from django.shortcuts import render, redirect
from homepage.models import ProjectShare, EnviromentCate, Account, Subject,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectshares = ProjectShare.objects.all()
            for projectshare in projectshares:
                projectshare.createdate = projectshare.createdate
                projectshare.editdate = projectshare.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'projectshares': projectshares}
            return render(request, 'adminprojectshare/projectshare_show.html', context)
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
                

                projectshare = ProjectShare( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid']),
                                        projectsharetopicname=request.POST['projectsharename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        description = request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        link=request.POST['link'],  
                                        viewcount=request.POST['viewcount'],  
                                        likecount=request.POST['likecount'],  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                projectshare.save()
                return redirect('/adminprojectshare/')
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
                    # 'subjectparts': subjectparts
                    'enviromentcates': enviromentcates,
                }
            
            return render(request, 'adminprojectshare/projectshare_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectshare = ProjectShare.objects.get(projectsharetopicid=id)
            projectshare.createdate = projectshare.createdate
            projectshare.editdate = datetime.now()

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
                'projectshare': projectshare,
                # 'subjectparts': subjectparts,
                'enviromentcates': enviromentcates,
            }
            
            return render(request, 'adminprojectshare/projectshare_edit.html', context)
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
            projectshare = ProjectShare.objects.filter(projectsharetopicid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            
            if request.POST.get('enviromentcateid')!= '0':
                projectshare = ProjectShare.objects.filter(projectsharetopicid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNum(request.POST['enviromentcateid'])))
            projectshare = ProjectShare.objects.get(projectsharetopicid=id)

            # Lấy url của avatar
            try:
                token_avatar = request.FILES['avatar']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = projectshare.avatar

            projectshare.projectsharetopicname=request.POST['projectsharename']
            projectshare.createdate=projectshare.createdate
            projectshare.editdate=datetime.now()
            projectshare.description=request.POST['description']
            projectshare.content=request.POST['content']
            projectshare.link=request.POST['link']
            projectshare.viewcount=request.POST['viewcount']
            projectshare.likecount=request.POST['likecount']
            projectshare.isenable=request.POST['isenable']
            projectshare.avatar=ava
            projectshare.note=request.POST['note']
            projectshare.save()
            return redirect('/adminprojectshare/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectshare = ProjectShare.objects.get(projectsharetopicid= id)
            projectshare.delete()
            return redirect('/adminprojectshare/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của subjectpart
# def validate_subjectprojectshare(request):
#     subject = request.GET.get('subject', None)
#     s = ''

#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True
        
#     if edit == True:
#         projectshare  = ProjectShare.objects.get(projectsharetopicid = request.GET.get('projectshare', None))
    
#     if edit == False or change == True:
#         s = '<option type="text" name="subjectpartid" value="">-- Chọn --</option>'
#         if(subject == "0"):
#             s = '<option type="text" name="subjectpartid" value="0">Chung</option>'
#     else:
#         if change == False:
#             if projectshare.subjectpartid != None:
#                 s= ' <option type="text" name="subjectpartid" value="' + str(projectshare.subjectpartid.subjectpartid) + ' ">' + projectshare.subjectpartid.subjectpartname + '</option>'
#             else:
#                 s= '<option type="text" name="subjectpartid" value="0">Chung</option>'
    
#     temp = ''
    
#     if subject == None:
#         subjectparts = None
#     else:
#         subjectparts = SubjectPart.objects.filter(subjectid=subject)
#         for subjectpart in subjectparts: 
#             if edit == True and change == False:
#                 if subjectpart.subjectpartid != projectshare.subjectpartid.subjectpartid:
#                         temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#             else:
#                 temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#             s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)