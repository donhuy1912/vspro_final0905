from django.shortcuts import render, redirect
from homepage.models import *
from datetime import datetime
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enrollments = Enrollment.objects.all()

            for enrollment in enrollments:
                enrollment.createdate = enrollment.createdate
                enrollment.editdate = enrollment.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'enrollments': enrollments}
            return render(request, 'adminenrollment/enrollment_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                enrollment = Enrollment( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                enrollment.save()
                return redirect('/adminenrollment/')
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
                    'accounts': accounts,
                    'subjects': subjects,
                }
            return render(request, 'adminenrollment/enrollment_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enrollment = Enrollment.objects.get(enrollmentid=id)
            enrollment.createdate = enrollment.createdate
            enrollment.editdate = datetime.now()

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
                'enrollment': enrollment
            }
            
            return render(request, 'adminenrollment/enrollment_edit.html', context)
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
            enrollment = Enrollment.objects.filter(enrollmentid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            enrollment = Enrollment.objects.filter(enrollmentid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            enrollment = Enrollment.objects.get(enrollmentid=id)
            enrollment.createdate = enrollment.createdate
            enrollment.editdate = datetime.now()
            enrollment.isenable = request.POST['isenable']
            enrollment.note = request.POST['note']
            enrollment.save()
            return redirect('/adminenrollment/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            enrollment = Enrollment.objects.get(enrollmentid= id)
            enrollment.delete()
            return redirect('/adminenrollment/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')