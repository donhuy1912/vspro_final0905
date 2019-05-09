from django.shortcuts import render, redirect
from homepage.models import Chapter, Subject, Account,UserDetail
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            chapters = Chapter.objects.all()
            for chapter in chapters:
                chapter.createdate = chapter.createdate
                chapter.editdate = chapter.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'chapters': chapters}
            return render(request, 'adminchapter/chapter_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                chapter = Chapter( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        chaptername = request.POST['chapterid'], 
                                        createdate = datetime.now(), 
                                        editdate = datetime.now(),
                                        description = request.POST['description'],
                                        content = request.POST['content'],
                                        order = request.POST['order'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                chapter.save()
                return redirect('/adminchapter/')
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
                
            return render(request, 'adminchapter/chapter_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            chapter = Chapter.objects.get(chapterid=id)
            chapter.createdate = chapter.createdate
            chapter.editdate = datetime.now()

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
                'chapter': chapter,
                'accounts': accounts,
                'subjects': subjects,
            }
            return render(request, 'adminchapter/chapter_edit.html', context)
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
            chapter = Chapter.objects.filter(chapterid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            chapter = Chapter.objects.filter(chapterid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            chapter = Chapter.objects.get(chapterid=id)
            chapter.chaptername=request.POST['chapterid']
            chapter.createdate=chapter.createdate
            chapter.editdate=datetime.now()
            chapter.description=request.POST['description']
            chapter.content=request.POST['content']
            chapter.order=request.POST['order']
            chapter.isenable=request.POST['isenable']
            chapter.note=request.POST['note']
            chapter.save()
            return redirect('/adminchapter/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            chapter = Chapter.objects.get(chapterid= id)
            chapter.delete()
            return redirect('/adminchapter/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


 #lấy giá trị item được nhập vào để gán giá trị cho order
def validate_subjectorderchapter(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    
    if len(chapters) == 0:
        s = 1
    else:
        listorder=[]
        for chapter in chapters:
            listorder.append(chapter.order) 
            
        s=max(listorder) + 1
    
    data = {
        'is_taken': s,
    }

    return JsonResponse(data)