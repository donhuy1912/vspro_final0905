from django.shortcuts import render, redirect
from homepage.models import ProjectShareLike, ProjectShare, Account
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectsharelikes = ProjectShareLike.objects.all()
            
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'projectsharelikes': projectsharelikes }
            return render(request, 'adminprojectsharelike/projectsharelike_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                projectsharelike = ProjectShareLike( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        projectsharetopicid = ProjectShare.objects.get(projectsharetopicid = request.POST['projectsharetopicid']),
                                        status=request.POST['status'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                projectsharelike.save()
                return redirect('/adminprojectsharelike/')
            else:
                projectshares = ProjectShare.objects.all()
                for projectshare in projectshares:
                    projectshare.createdate = projectshare.createdate
                    projectshare.editdate = projectshare.editdate

                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate

                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'projectshares': projectshares,
                    'accounts': accounts,
                }
            return render(request, 'adminprojectsharelike/projectsharelike_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectsharelike = ProjectShareLike.objects.get(projectsharelikeid=id)

            projectshares = ProjectShare.objects.all()
            for projectshare in projectshares:
                projectshare.createdate = projectshare.createdate
                projectshare.editdate = projectshare.editdate

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'projectsharelike': projectsharelike,
                'projectshares': projectshares,
                'accounts': accounts,
            }
            return render(request, 'adminprojectsharelike/projectsharelike_edit.html', context)
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
            projectsharelike = ProjectShareLike.objects.filter(projectsharelikeid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            projectsharelike = ProjectShareLike.objects.filter(projectsharelikeid = id).update(projectsharetopicid = ProjectShare.objects.get(projectsharetopicid = getNum(request.POST['projectsharetopicid'])))
            projectsharelike = ProjectShareLike.objects.get(projectsharelikeid=id)
            projectsharelike.status=request.POST['status']
            projectsharelike.isenable=request.POST['isenable']
            projectsharelike.note=request.POST['note']
            projectsharelike.save()
            return redirect('/adminprojectsharelike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            projectsharelike = ProjectShareLike.objects.get(projectsharelikeid= id)
            projectsharelike.delete()
            return redirect('/adminprojectsharelike/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')