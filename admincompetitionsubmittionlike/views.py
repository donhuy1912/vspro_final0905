from django.shortcuts import render, redirect
from homepage.models import CompetitionSubmittionLike, CompetitionSubmittion, Account, Competition,UserDetail
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittionlikes = CompetitionSubmittionLike.objects.all()
            
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'competitionsubmittionlikes': competitionsubmittionlikes }
            return render(request, 'admincompetitionsubmittionlike/competitionsubmittionlike_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                competitionsubmittionlike = CompetitionSubmittionLike( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        competitionsubmittionid = CompetitionSubmittion.objects.get(competitionsubmittionid = request.POST['competitionsubmittionid']),
                                        status=request.POST['status'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                competitionsubmittionlike.save()
                return redirect('/admincompetitionsubmittionlike/')
            else:
                competitionsubmittions = CompetitionSubmittion.objects.all()
                for competitionsubmittion in competitionsubmittions:
                    competitionsubmittion.createdate = competitionsubmittion.createdate
                    competitionsubmittion.editdate = competitionsubmittion.editdate
                
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                competitions = Competition.objects.all()
                for competition in competitions:
                    competition.createdate = competition.createdate
                    competition.editdate = competition.editdate

                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'competitionsubmittions': competitionsubmittions,
                    'accounts': accounts,
                    'competitions': competitions,
                }
            return render(request, 'admincompetitionsubmittionlike/competitionsubmittionlike_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittionlike = CompetitionSubmittionLike.objects.get(competitionsubmittionlikeid=id)
            

            competitionsubmittions = CompetitionSubmittion.objects.all()
            for competitionsubmittion in competitionsubmittions:
                competitionsubmittion.createdate = competitionsubmittion.createdate
                competitionsubmittion.editdate = competitionsubmittion.editdate

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            competitions = Competition.objects.all()
            for competition in competitions:
                competition.createdate = competition.createdate
                competition.editdate = competition.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'competitionsubmittionlike': competitionsubmittionlike,
                'competitionsubmittions': competitionsubmittions,
                'accounts': accounts,    
                'competitions': competitions,
            }
            return render(request, 'admincompetitionsubmittionlike/competitionsubmittionlike_edit.html', context)
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
            competitionsubmittionlike = CompetitionSubmittionLike.objects.filter(competitionsubmittionlikeid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            competitionsubmittionlike = CompetitionSubmittionLike.objects.filter(competitionsubmittionlikeid = id).update(competitionsubmittionid = CompetitionSubmittion.objects.get(competitionsubmittionid = getNum(request.POST['competitionsubmittionid'])))
            competitionsubmittionlike = CompetitionSubmittionLike.objects.get(competitionsubmittionlikeid=id)
            competitionsubmittionlike.status=request.POST['status']
            competitionsubmittionlike.isenable=request.POST['isenable']
            competitionsubmittionlike.note=request.POST['note']
            competitionsubmittionlike.save()
            return redirect('/admincompetitionsubmittionlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            competitionsubmittionlike = CompetitionSubmittionLike.objects.get(competitionsubmittionlikeid= id)
            competitionsubmittionlike.delete()
            return redirect('/admincompetitionsubmittionlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị competition được nhập vào để giới hạn giá trị show ra của competitionsubmittion
def validate_competitioncompetitionsubmittionlike(request):
    competition = request.GET.get('competition', None)
    competitionsubmittions = CompetitionSubmittion.objects.filter(competitionid=competition)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
    
    if edit == True:
        competitionsubmittionlike  = CompetitionSubmittionLike.objects.get(competitionsubmittionlikeid = request.GET.get('competitionsubmittionlike', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="competitionsubmittionid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="competitionsubmittionid" value="' + str(competitionsubmittionlike.competitionsubmittionid.competitionsubmittionid) + ' ">' + competitionsubmittionlike.competitionsubmittionid.description + '</option>'
    temp = ''

    for competitionsubmittion in competitionsubmittions: 
        if edit == True and change == False:
            if competitionsubmittion.competitionsubmittionid != competitionsubmittionlike.competitionsubmittionid.competitionsubmittionid:
                    temp = ' <option type="text" name="competitionsubmittionid" value="' + str(competitionsubmittion.competitionsubmittionid) + ' ">' + competitionsubmittion.description + '</option>'
        else:
            temp = ' <option type="text" name="competitionsubmittionid" value="' + str(competitionsubmittion.competitionsubmittionid) + ' ">' + competitionsubmittion.description + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)