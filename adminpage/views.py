from django.shortcuts import render, redirect
from homepage.models import *
# Create your views here.
class chartyearmoth:
    m1=0
    m2=0
    m3=0
    m4=0
    m5=0
    m6=0
    m7=0
    m8=0
    m9=0
    m10=0
    m11=0
    m12=0

class envirper:
    name='Noname'
    count=0
    

def admin1 (request):
    if request.session.has_key('username'):
        username = request.session['username']
        account = Account.objects.get(username=username)
        if account.accounttypeid.accounttypeid == 1:
            chartyear=chartyearmoth()
            accounts=Account.objects.all()
            countaccount=len(accounts)
            userdetail=UserDetail.objects.get(accountid=account)
            countadmin=len(Account.objects.filter(accounttypeid=1))
            countteacher=len(Account.objects.filter(accounttypeid=2))
            countstudent=len(Account.objects.filter(accounttypeid=3))
            countenvir=len(EnviromentCate.objects.all())
            countdcourse=len(Subject.objects.all())
            allenrolment= Enrollment.objects.all()
            for enrol in allenrolment:
                if enrol.createdate.month == 1:
                    chartyear.m1+=1
                elif enrol.createdate.month == 2:
                    chartyear.m2+=1
                elif enrol.createdate.month == 3:
                    chartyear.m3+=1
                elif enrol.createdate.month == 4:
                    chartyear.m4+=1
                elif enrol.createdate.month == 5:
                    chartyear.m5+=1
                elif enrol.createdate.month == 6:
                    chartyear.m6+=1
                elif enrol.createdate.month == 7:
                    chartyear.m7+=1
                elif enrol.createdate.month == 8:
                    chartyear.m8+=1
                elif enrol.createdate.month == 9:
                    chartyear.m9+=1
                elif enrol.createdate.month == 10:
                    chartyear.m10+=1
                elif enrol.createdate.month == 11:
                    chartyear.m11+=1
                elif enrol.createdate.month == 12:
                    chartyear.m12+=1
            envirs=EnviromentCate.objects.all()
            allenrols=Enrollment.objects.all()
            arrenvirper=[]
            for envir in envirs:
                subjects=Subject.objects.filter(enviromentcateid=envir)
                arrsub=[]
                for subject in subjects:
                    arrsub.append(subject.subjectid)
                enrols=Enrollment.objects.filter(subjectid__in=arrsub)
                temp=envirper()
                temp.name=envir.enviromentcatename
                temp.count=round(len(enrols)/(len(allenrols))*100,1)
                arrenvirper.append(temp)
                print(temp.name)
                print(temp.count)
                                    
            context={
                'arrenvirper':arrenvirper,
                'chartyear':chartyear,
                'countaccount':countaccount,
                'userdetail':userdetail,
                'countenvir':countenvir,
                'countcourse':countdcourse,
                'countadmin':countadmin,
                'countteacher':countteacher,
                'countstudent':countstudent,
                'account':account,
            }
            return render(request, 'adminpage/admin1.html',context)    
        else:
           return redirect('homepage:index') 
    else:
        return redirect('homepage:index')
    

def admin2 (request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            return render(request, 'adminpage/admin2.html')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
