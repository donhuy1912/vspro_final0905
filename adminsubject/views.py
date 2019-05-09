from django.shortcuts import render, redirect
from homepage.models import Subject, Account, EnviromentCate,UserDetail
from datetime import datetime
from homepage.myfunction import *

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjects = Subject.objects.all()
            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'subjects': subjects}
            return render(request, 'adminsubject/subject_show.html', context)
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
                    token_avatar = request.FILES['avatar']
                except:
                    token_avatar = None
                ava = ''
                if token_avatar != None:
                    ava = tokenFile(token_avatar)

                subject = Subject( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid']),
                                        subjectname=request.POST['subjectname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        introvideo=request.POST['video'],  
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                subject.save()
                return redirect('/adminsubject/')
            else:
                accounts = Account.objects.all()
                enviromentcates = EnviromentCate.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate

                for enviromentcate in enviromentcates:
                    enviromentcate.createdate = enviromentcate.createdate
                    enviromentcate.editdate = enviromentcate.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts':accounts,
                    'enviromentcates':enviromentcates,
                }
            return render(request, 'adminsubject/subject_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subject = Subject.objects.get(subjectid=id)
            subject.createdate = subject.createdate
            subject.editdate = datetime.now()

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            enviromentcates = EnviromentCate.objects.all()
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = enviromentcate.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'subject': subject,
                'accounts': accounts,
                'enviromentcates' : enviromentcates,
            }
            return render(request, 'adminsubject/subject_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def getNumber(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subject = Subject.objects.filter(subjectid = id).update(accountid = Account.objects.get(accountid = getNumber(request.POST['accountid'])))
            subject = Subject.objects.filter(subjectid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNumber(request.POST['enviromentcateid'])))
            subject = Subject.objects.get(subjectid=id)
            subject.subjectname=request.POST['subjectname']
            subject.createdate=subject.createdate
            subject.editdate=datetime.now()
            subject.introvideo=request.POST['video']
            subject.description=request.POST['description']
            subject.content=request.POST['content']
            subject.avatar=request.POST['avatar']
            subject.isenable=request.POST['isenable']
            subject.note=request.POST['note']
            subject.save()
            return redirect('/adminsubject/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subject = Subject.objects.get(subjectid= id)
            subject.delete()
            return redirect('/adminsubject/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')