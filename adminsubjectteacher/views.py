from django.shortcuts import render, redirect
from homepage.models import *
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectteachers = SubjectTeacher.objects.all()
        
            for subjectteacher in subjectteachers:
                subjectteacher.createdate = subjectteacher.createdate
                subjectteacher.editdate = subjectteacher.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'subjectteachers': subjectteachers}
            return render(request, 'adminsubjectteacher/subjectteacher_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                subjectteacher = SubjectTeacher( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                subjectteacher.save()
                return redirect('/adminsubjectteacher/')
            else:
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
                    'accounts':accounts,
                    'subjects':subjects,
                }
            return render(request, 'adminsubjectteacher/subjectteacher_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectteacher = SubjectTeacher.objects.get(subjectteacherid=id)
            subjectteacher.createdate = subjectteacher.createdate
            subjectteacher.editdate = datetime.now()

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
                'subjectteacher': subjectteacher,
                'accounts':accounts,
                'subjects':subjects,
            }
            return render(request, 'adminsubjectteacher/subjectteacher_edit.html', context)
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
            subjectteacher = SubjectTeacher.objects.filter(subjectteacherid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            subjectteacher = SubjectTeacher.objects.filter(subjectteacherid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            subjectteacher = SubjectTeacher.objects.get(subjectteacherid=id)
            subjectteacher.createdate = subjectteacher.createdate
            subjectteacher.editdate = datetime.now()
            subjectteacher.isenable = request.POST['isenable']
            subjectteacher.note = request.POST['note']
            subjectteacher.save()
            return redirect('/adminsubjectteacher/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectteacher = SubjectTeacher.objects.get(subjectteacherid= id)
            subjectteacher.delete()
            return redirect('/adminsubjectteacher/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')