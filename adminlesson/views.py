from django.shortcuts import render, redirect
from django.http import JsonResponse
from homepage.models import Lesson, Chapter, Account, Subject,UserDetail
from datetime import datetime

# Create your views here.


def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lessons = Lesson.objects.all()
            for lesson in lessons:
                lesson.createdate = lesson.createdate
                lesson.editdate = lesson.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'lessons': lessons}
            return render(request, 'adminlesson/lesson_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                lesson = Lesson(
                    accountid=Account.objects.get(accountid=request.POST['accountid']),
                    chapterid=Chapter.objects.get(chapterid=request.POST['chapterid']),
                    lessonname=request.POST['lessonname'],
                    createdate=datetime.now(),
                    editdate=datetime.now(),
                    description=request.POST['description'],
                    content=request.POST['content'],
                    order=request.POST['order'],
                    isenable=request.POST['isenable'],
                    note=request.POST['note'])
                lesson.save()
                return redirect('/adminlesson/')
            else:
                chapters = Chapter.objects.all()
                accounts = Account.objects.all()
                subjects = Subject.objects.all()
                for chapter in chapters:
                    chapter.createdate = chapter.createdate
                    chapter.editdate = chapter.editdate

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

            return render(request, 'adminlesson/lesson_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lesson = Lesson.objects.get(lessonid=id)
            lesson.createdate = lesson.createdate
            lesson.editdate = datetime.now()

            chapters = Chapter.objects.all()
            accounts = Account.objects.all()
            subjects = Subject.objects.all()
            subjectid = lesson.chapterid.subjectid
            for chapter in chapters:
                chapter.createdate = chapter.createdate
                chapter.editdate = chapter.editdate

            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,'lesson': lesson,
                    'chapters': chapters,
                    'subjects': subjects,
                    'accounts': accounts,
                    'subjectid': subjectid,
                    }
            return render(request, 'adminlesson/lesson_edit.html', context)
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
            lesson = Lesson.objects.filter(lessonid=id).update(accountid=Account.objects.get(accountid=getNum(request.POST['accountid'])))
            lesson = Lesson.objects.filter(lessonid=id).update(chapterid=Chapter.objects.get(chapterid=getNum(request.POST['chapterid'])))
            lesson = Lesson.objects.get(lessonid=id)
            lesson.lessonname = request.POST['lessonname']
            lesson.createdate = lesson.createdate
            lesson.editdate = datetime.now()
            lesson.description = request.POST['description']
            lesson.content = request.POST['content']
            lesson.order = request.POST['order']
            lesson.isenable = request.POST['isenable']
            lesson.note = request.POST['note']
            lesson.save()
            return redirect('/adminlesson/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lesson = Lesson.objects.get(lessonid=id)
            lesson.delete()
            return redirect('/adminlesson/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


# lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
def validate_subjectlesson(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)

    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        lesson  = Lesson.objects.get(lessonid = request.GET.get('lesson', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="chapterid" value="' + str(lesson.chapterid.chapterid) + ' ">' + lesson.chapterid.chaptername + '</option>'
    
    temp = ''

    for chapter in chapters: 
        if edit == True and change == False:
            if chapter.chapterid!=lesson.chapterid.chapterid:
                    temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        else:
            temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)




#lấy giá trị subject được nhập vào để gán giá trị cho order
def validate_subjectorderlesson(request):
    subject = request.GET.get('subject', None)
    # chap = request.GET.get('chap', None)  //đang làm load order cho phần edit
    # choosenchap = request.GET.get('choosenchap', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    # les = Lesson.objects.get(lessonid = request.GET.get('les', None))
    # t = False
   
    if len(chapters) == 0:
        s = 1
    else:
        listorder=[]
        for chapter in chapters:
            lessons = Lesson.objects.filter(chapterid = chapter.chapterid)
            for lesson in lessons:
                listorder.append(lesson.order)   
        s=1
        if listorder != []:
            s=max(listorder) + 1
       
    data = {
        'is_taken': s,
    }

    return JsonResponse(data)


#lấy giá trị subject được nhập vào để gán giá trị cho order
def validate_chapterorderlesson(request):
    subject = request.GET.get('subject', None)
    chap = request.GET.get('chap', None)  
    choosenchap = request.GET.get('chapter', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    les = Lesson.objects.get(lessonid = request.GET.get('les', None))

    if len(chapters) == 0:
        s = 1
    else:
        if int(chap) == int(choosenchap):
            s = les.order
        else:
            t = False
            listorder=[]
            for chapter in chapters:
                lessons = Lesson.objects.filter(chapterid = chapter)
                for lesson in lessons:
                    listorder.append(lesson.order) 
            s=max(listorder) + 1

    data = {
        'is_taken': s,
    }

    return JsonResponse(data)
