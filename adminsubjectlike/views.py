from django.shortcuts import render, redirect
from homepage.models import SubjectLike, Subject, Account, Subject,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectlikes = SubjectLike.objects.all()
            # for subjectlike in subjectlikes:
            #     subjectlike.createdate = subjectlike.createdate
            #     subjectlike.editdate = subjectlike.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,'subjectlikes': subjectlikes }
            return render(request, 'adminsubjectlike/subjectlike_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                subjectlike = SubjectLike( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        status=request.POST['status'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                subjectlike.save()
                return redirect('/adminsubjectlike/')
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
            return render(request, 'adminsubjectlike/subjectlike_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectlike = SubjectLike.objects.get(subjectlikeid=id)
            
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
                'subjectlike': subjectlike
            }

            return render(request, 'adminsubjectlike/subjectlike_edit.html', context)
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
            subjectlike = SubjectLike.objects.filter(subjectlikeid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            subjectlike = SubjectLike.objects.filter(subjectlikeid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            subjectlike = SubjectLike.objects.get(subjectlikeid=id)
            subjectlike.status=request.POST['status']
            subjectlike.isenable=request.POST['isenable']
            subjectlike.note=request.POST['note']
            subjectlike.save()
            return redirect('/adminsubjectlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectlike = SubjectLike.objects.get(subjectlikeid= id)
            subjectlike.delete()
            return redirect('/adminsubjectlike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')