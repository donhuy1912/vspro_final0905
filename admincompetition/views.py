from django.shortcuts import render, redirect
from homepage.models import Competition, EnviromentCate, Account, Subject,UserDetail
from datetime import datetime
from django.http import JsonResponse
from homepage.myfunction import tokenFile

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitions = Competition.objects.all()
            for competition in competitions:
                competition.createdate = competition.createdate
                competition.editdate = competition.editdate
                competition.opendate = competition.opendate.strftime("%Y-%m-%d %H:%M:%S")
                competition.enddate = competition.enddate.strftime("%Y-%m-%d %H:%M:%S")
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'competitions': competitions}
            return render(request, 'admincompetition/competition_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':     
                    #Lấy url của avatar
                try:
                    token_avatar = request.FILES['image']
                except:
                    token_avatar = None
                ava = ''
                if token_avatar != None:
                    ava = tokenFile(token_avatar)

                competition = Competition( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid']),
                                        competitionname=request.POST['competitionname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        opendate= request.POST['opendate'],
                                        enddate= request.POST['enddate'],
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        viewcount=request.POST['viewcount'],  
                                        likecount=request.POST['likecount'],  
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                competition.save()
                return redirect('/admincompetition/')
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
            
            return render(request, 'admincompetition/competition_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competition = Competition.objects.get(competitionid=id)
            competition.createdate = competition.createdate
            competition.editdate = datetime.now()
            competition.opendate = competition.opendate.strftime("%Y-%m-%d %H:%M:%S")
            competition.enddate = competition.enddate.strftime("%Y-%m-%d %H:%M:%S")

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
                'competition': competition,
                # 'subjectparts': subjectparts,
                'enviromentcates': enviromentcates,
            }

            return render(request, 'admincompetition/competition_edit.html', context)
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
            competition = Competition.objects.filter(competitionid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            competition = Competition.objects.filter(competitionid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNum(request.POST['enviromentcateid'])))
            competition = Competition.objects.get(competitionid=id)
            
            #Lấy url của avatar
            try:
                token_avatar = request.FILES['image']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = competition.avatar

            if request.POST['opendate'] == '':
                opendate = competition.opendate
            else:
                opendate = request.POST['opendate']
            if request.POST['enddate'] == '':
                enddate = competition.enddate
            else:
                enddate = request.POST['enddate']
                
            competition.competitionname=request.POST['competitionname']
            competition.createdate=competition.createdate
            competition.editdate=datetime.now()
            competition.opendate= opendate
            competition.enddate= enddate
            competition.description=request.POST['description']
            competition.content=request.POST['content']
            competition.avatar=ava
            competition.viewcount=request.POST['viewcount']
            competition.likecount=request.POST['likecount']
            competition.isenable=request.POST['isenable']
            competition.note=request.POST['note']
            competition.save()
            return redirect('/admincompetition/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competition = Competition.objects.get(competitionid= id)
            competition.delete()
            return redirect('/admincompetition/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của subjectpart
# def validate_subjectcompetition(request):
#     subject = request.GET.get('subject', None)
#     subjectparts = SubjectPart.objects.filter(subjectid=subject)
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True
        
#     if edit == True:
#         competition  = Competition.objects.get(competitionid = request.GET.get('competition', None))
    
#     if edit == False or change == True:
#         s = '<option type="text" name="subjectpartid" value="">-- Chọn --</option>'
#         if(subject == "0"):
#             s = '<option type="text" name="subjectpartid" value="0">Chung</option>'
#     else:
#         if change == False:
#             if competition.subjectpartid != None:
#                 s= ' <option type="text" name="subjectpartid" value="' + str(competition.subjectpartid.subjectpartid) + ' ">' + competition.subjectpartid.subjectpartname + '</option>'
#             else:
#                 s= '<option type="text" name="subjectpartid" value="0">Chung</option>'
#     temp = ''

#     for subjectpart in subjectparts: 
#         if edit == True and change == False:
#             if subjectpart.subjectpartid != competition.subjectpartid.subjectpartid:
#                     temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         else:
#             temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)