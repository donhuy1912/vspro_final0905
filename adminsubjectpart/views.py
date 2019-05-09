from django.shortcuts import render, redirect
from homepage.models import SubjectPart, Subject, Account,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectparts = SubjectPart.objects.all()
            for subjectpart in subjectparts:
                subjectpart.createdate = subjectpart.createdate
                subjectpart.editdate = subjectpart.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'subjectparts': subjectparts}
            return render(request, 'adminsubjectpart/subjectpart_show.html', context)
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
                subjectpart = SubjectPart( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        subjectpartname=request.POST['subjectpartname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        order=request.POST['order'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                subjectpart.save()
                return redirect('/adminsubjectpart/')
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
                    'subjects': subjects
                }
            return render(request, 'adminsubjectpart/subjectpart_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectpart = SubjectPart.objects.get(subjectpartid=id)
            subjectpart.createdate = subjectpart.createdate
            subjectpart.editdate = datetime.now()

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
                'subjectpart': subjectpart,
                'accounts': accounts,
                'subjects': subjects

            }
            return render(request, 'adminsubjectpart/subjectpart_edit.html', context)
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
            subjectpart = SubjectPart.objects.get(subjectpartid = id)
            try:
                token_avatar = request.FILES['avatar']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = subjectpart.avatar

            subjectpart = SubjectPart.objects.filter(subjectpartid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            subjectpart = SubjectPart.objects.filter(subjectpartid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            subjectpart = SubjectPart.objects.get(subjectpartid=id)
            subjectpart.subjectpartname=request.POST['subjectpartname']
            subjectpart.createdate=subjectpart.createdate
            subjectpart.editdate=datetime.now()
            subjectpart.avatar=ava
            subjectpart.description=request.POST['description']
            subjectpart.content=request.POST['content']
            subjectpart.order=request.POST['order']
            subjectpart.isenable=request.POST['isenable']
            subjectpart.note=request.POST['note']
            subjectpart.save()
            return redirect('/adminsubjectpart/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            subjectpart = SubjectPart.objects.get(subjectpartid= id)
            subjectpart.delete()
            return redirect('/adminsubjectpart/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị item được nhập vào để gán giá trị cho order
def validate_subjectsubjectpart(request):
    subject = request.GET.get('subject', None)
    sub = request.GET.get('sub', None)
    subjectparts = SubjectPart.objects.filter(subjectid=subject)
    subpart = SubjectPart.objects.get(subjectpartid = request.GET.get('subpart', None))
    
    if len(subjectparts) == 0:
        s = 1
    else:
        listorder = []
        if int(subject) == int(sub):
            s = subpart.order
        else:
            for subjectpart in subjectparts:
                listorder.append(subjectpart.order)
            s = max(listorder) + 1
   
    data = {
        'is_taken': s,
    }

    return JsonResponse(data)
