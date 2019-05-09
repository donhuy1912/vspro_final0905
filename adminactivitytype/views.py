from django.shortcuts import render, redirect
from homepage.models import ActivityType, Account,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitytypes = ActivityType.objects.all()
            for activitytype in activitytypes:
                #activitytype.createdate = activitytype.createdate.strftime("%Y-%m-%d")
                activitytype.createdate = activitytype.createdate
                activitytype.editdate = activitytype.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                 'activitytypes': activitytypes}
            return render(request, 'adminactivitytype/activitytype_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                activitytype = ActivityType( 
                                        activitytypename=request.POST['activitytypename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                activitytype.save()
                return redirect('/adminactivitytype/')
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,}
            return render(request, 'adminactivitytype/activitytype_create.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitytype = ActivityType.objects.get(activitytypeid=id)
            activitytype.createdate = activitytype.createdate
            activitytype.editdate = datetime.now()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'activitytype': activitytype}
            return render(request, 'adminactivitytype/activitytype_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def us_date_to_iso(us_date):
    return '{2}-{0:>02}-{1:>02}'.format(*us_date.split('/'))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitytype = ActivityType.objects.get(activitytypeid=id)
            activitytype.activitytypename=request.POST['activitytypename']
            activitytype.createdate=activitytype.createdate
            activitytype.editdate=datetime.now()
            activitytype.isenable=request.POST['isenable']
            activitytype.note=request.POST['note']
            activitytype.save()
            return redirect('/adminactivitytype/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitytype = ActivityType.objects.get(activitytypeid= id)
            activitytype.delete()
            return redirect('/adminactivitytype/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')