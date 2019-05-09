from django.shortcuts import render, redirect
from homepage.models import CompetitionSubmittion, Competition, Account, EnviromentCate,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittions = CompetitionSubmittion.objects.all()
            for competitionsubmittion in competitionsubmittions:
                competitionsubmittion.createdate = competitionsubmittion.createdate
                competitionsubmittion.editdate = competitionsubmittion.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'competitionsubmittions': competitionsubmittions}
            return render(request, 'admincompetitionsubmittion/competitionsubmittion_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                try:
                    token_link = request.FILES['link']
                except:
                    token_link = None
                lin = ''
                if token_link != None:
                    lin = tokenFile(token_link)
                competitionsubmittion = CompetitionSubmittion( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        # enviromentcateid = Account.objects.get(accountid = request.POST['enviromentcateid']),
                                        competitionid = Competition.objects.get(competitionid = request.POST['competitionid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        link=lin,
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                competitionsubmittion.save()
                return redirect('/admincompetitionsubmittion/')
            else:
                competitions = Competition.objects.all()
                for competition in competitions:
                    competition.createdate = competition.createdate
                    competition.editdate = competition.editdate
                    competition.opendate = competition.opendate.strftime("%Y-%m-%d %H:%M:%S")
                    competition.enddate = competition.enddate.strftime("%Y-%m-%d %H:%M:%S")
                
                accounts = Account.objects.all()
                # subjects = Subject.objects.all()
                enviromentcates = EnviromentCate.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate

                # for subject in subjects:
                #     subject.createdate = subject.createdate
                #     subject.editdate = subject.editdate
                
                for enviromentcate in enviromentcates:
                    enviromentcate.createdate = enviromentcate.createdate
                    enviromentcate.editdate = enviromentcate.editdate

                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts,
                    # 'subjects': subjects,
                    'competitions': competitions,
                    'enviromentcates': enviromentcates,
                }
            
            return render(request, 'admincompetitionsubmittion/competitionsubmittion_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittion = CompetitionSubmittion.objects.get(competitionsubmittionid=id)
            competitionsubmittion.createdate = competitionsubmittion.createdate
            competitionsubmittion.editdate = datetime.now()


            competitions = Competition.objects.all()
            for competition in competitions:
                competition.createdate = competition.createdate
                competition.editdate = competition.editdate
                competition.opendate = competition.opendate.strftime("%Y-%m-%d %H:%M:%S")
                competition.enddate = competition.enddate.strftime("%Y-%m-%d %H:%M:%S")
            
            accounts = Account.objects.all()
            # subjects = Subject.objects.all()
            enviromentcates = EnviromentCate.objects.all()

            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            # for subject in subjects:
            #     subject.createdate = subject.createdate
            #     subject.editdate = subject.editdate
            
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = enviromentcate.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounts': accounts,
                # 'subjects': subjects,
                'competitionsubmittion': competitionsubmittion,
                'competitions': competitions,
                'enviromentcates': enviromentcates,
            }
        
            return render(request, 'admincompetitionsubmittion/competitionsubmittion_edit.html', context)
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
            competitionsubmittion = CompetitionSubmittion.objects.filter(competitionsubmittionid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            # competitionsubmittion = CompetitionSubmittion.objects.filter(competitionsubmittionid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNum(request.POST['enviromentcateid'])))
            competitionsubmittion = CompetitionSubmittion.objects.filter(competitionsubmittionid = id).update(competitionid = Competition.objects.get(competitionid = getNum(request.POST['competitionid'])))
            competitionsubmittion = CompetitionSubmittion.objects.get(competitionsubmittionid=id)

            try:
                token_link = request.FILES['link']
            except:
                token_link = None
            lin = ''
            if token_link != None:
                lin = tokenFile(token_link)
            else:
                lin = competitionsubmittion.link

            competitionsubmittion.createdate=competitionsubmittion.createdate
            competitionsubmittion.editdate=datetime.now()
            competitionsubmittion.link=lin
            competitionsubmittion.description=request.POST['description']
            competitionsubmittion.content=request.POST['content']
            competitionsubmittion.isenable=request.POST['isenable']
            competitionsubmittion.note=request.POST['note']
            competitionsubmittion.save()
            return redirect('/admincompetitionsubmittion/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittion = CompetitionSubmittion.objects.get(competitionsubmittionid= id)
            competitionsubmittion.delete()
            return redirect('/admincompetitionsubmittion/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


# def validate_subjectcompetitionsubmittion(request):
#     subject = request.GET.get('subject', None)
#     subjectparts = SubjectPart.objects.filter(subjectid=subject)
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True
        
#     if edit == True:
#         competitionsubmittion  = CompetitionSubmittion.objects.get(competitionsubmittionid = request.GET.get('competitionsubmittion', None))
    
#     if edit == False or change == True:
#         s = '<option type="text" name="subjectpartid" value="">-- Chọn --</option>'
#         if(subject == "0"):
#             s = '<option type="text" name="subjectpartid" value="0">Chung</option>'
#     else:
#         if change == False:
#             if competitionsubmittion.subjectpartid != None:
#                 s= ' <option type="text" name="subjectpartid" value="' + str(competitionsubmittion.subjectpartid.subjectpartid) + ' ">' + competitionsubmittion.subjectpartid.subjectpartname + '</option>'
#             else:
#                 s= '<option type="text" name="subjectpartid" value="0">Chung</option>'
#     temp = ''

#     for subjectpart in subjectparts: 
#         if edit == True and change == False:
#             if subjectpart.subjectpartid != competitionsubmittion.subjectpartid.subjectpartid:
#                     temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         else:
#             temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)

def validate_enviromentcatecompetitionsubmittion(request):
    enviromentcate = request.GET.get('enviromentcate', None)
   
    competitions = Competition.objects.filter(enviromentcateid=enviromentcate)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
    if edit == True:
        competitionsubmittion  = CompetitionSubmittion.objects.get(competitionsubmittionid = request.GET.get('competitionsubmittion', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="competitionid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="competitionid" value="' + str(competitionsubmittion.competitionid.competitionid) + ' ">' + competitionsubmittion.competitionid.competitionname + '</option>'
    
    temp = ''

    for competition in competitions: 
        if edit == True and change == False:
            if competition.competitionid != competitionsubmittion.competitionid.competitionid:
                    temp = ' <option type="text" name="competitionid" value="' + str(competition.competitionid) + ' ">' + competition.competitionname + '</option>'
        else:
            temp = ' <option type="text" name="competitionid" value="' + str(competition.competitionid) + ' ">' + competition.competitionname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)
