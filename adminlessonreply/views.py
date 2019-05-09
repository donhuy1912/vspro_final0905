from django.shortcuts import render, redirect
from homepage.models import LessonReply, Enrollment, Lesson, Chapter, Subject, Account,UserDetail
from datetime import datetime
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lessonreplys = LessonReply.objects.all()
            for lessonreply in lessonreplys:
                lessonreply.createdate = lessonreply.createdate
                lessonreply.editdate = lessonreply.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'lessonreplys': lessonreplys}
            return render(request, 'adminlessonreply/lessonreply_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                lessonreply = LessonReply( 
                                        enrollmentid = Enrollment.objects.get(enrollmentid = request.POST['accountid']),
                                        lessonid = Lesson.objects.get(lessonid = request.POST['lessonid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                lessonreply.save()
                return redirect('/adminlessonreply/')
            else:
                lessons = Lesson.objects.all()
                for lesson in lessons:
                    lesson.createdate = lesson.createdate
                    lesson.editdate = lesson.editdate

                enrollments = Enrollment.objects.all()
                accounts = Account.objects.all()
                subjects = Subject.objects.all()
                
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                for enrollment in enrollments:
                    enrollment.createdate = enrollment.createdate
                    enrollment.editdate = enrollment.editdate

                for subject in subjects:
                    subject.createdate = subject.createdate
                    subject.editdate = subject.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'enrollments': enrollments,
                    'subjects': subjects,
                    'lessons': lessons,
                    'accounts': accounts,
                }
                
            return render(request, 'adminlessonreply/lessonreply_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lessonreply = LessonReply.objects.get(lessonreplyid=id)
            lessonreply.createdate = lessonreply.createdate
            lessonreply.editdate = datetime.now()

            lessons = Lesson.objects.all()
            for lesson in lessons:
                lesson.createdate = lesson.createdate
                lesson.editdate = lesson.editdate
                
            enrollments = Enrollment.objects.all()
            accounts = Account.objects.all()
            subjects = Subject.objects.all()
                
            for enrollment in enrollments:
                enrollment.createdate = enrollment.createdate
                enrollment.editdate = enrollment.editdate
            
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
                'enrollments': enrollments,
                'subjects': subjects,
                'lessonreply': lessonreply,
                'lessons': lessons,
                'accounts': accounts,   
            }

            return render(request, 'adminlessonreply/lessonreply_edit.html', context)
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
            lessonreply = LessonReply.objects.filter(lessonreplyid = id).update(enrollmentid = Enrollment.objects.get(enrollmentid = getNum(request.POST['accountid'])))
            lessonreply = LessonReply.objects.filter(lessonreplyid = id).update(lessonid = Lesson.objects.get(lessonid = getNum(request.POST['lessonid'])))
            lessonreply = LessonReply.objects.get(lessonreplyid=id)
            lessonreply.createdate=lessonreply.createdate
            lessonreply.editdate=datetime.now()
            lessonreply.content=request.POST['content']
            lessonreply.isenable=request.POST['isenable']
            lessonreply.note=request.POST['note']
            lessonreply.save()
            return redirect('/adminlessonreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            lessonreply = LessonReply.objects.get(lessonreplyid= id)
            lessonreply.delete()
            return redirect('/adminlessonreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
# def validate_subjectlessonreply(request):
#     subject = request.GET.get('subject',None)
#     chapters = Chapter.objects.filter(subjectid = subject)
#     s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
#     temp = ''
#     for chapter in chapters:
#         temp = '<option type="text" name="chapterid" value=" ' + str(chapter.chapterid) + ' "> ' + chapter.chaptername + ' </option'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data)

def validate_subjectlessonreply(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
        
    if edit == True:
        lessonreply  = LessonReply.objects.get(lessonreplyid = request.GET.get('lessonreply', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="chapterid" value="' + str(lessonreply.lessonid.chapterid.chapterid) + ' ">' + lessonreply.lessonid.chapterid.chaptername + '</option>'
    
    temp = ''

    for chapter in chapters: 
        if edit == True and change == False:
            if chapter.chapterid != lessonreply.lessonid.chapterid.chapterid:
                    temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        else:
            temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
# def validate_chapterlessonreply(request):
#     chapter = request.GET.get('chapter', None)
#     lessons = Lesson.objects.filter(chapterid = chapter)
#     s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
#     temp = ''
#     for lesson in lessons:
#         temp = '<option type="text" name="lessonid" value=" ' + str(lesson.lessonid) + ' "> ' + lesson.lessonname + ' </option'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data) 


def validate_chapterlessonreply(request):
    chapter = request.GET.get('chapter', None)
    lessons = Lesson.objects.filter(chapterid=chapter)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        lessonreply = LessonReply.objects.get(lessonreplyid = request.GET.get('lessonreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="lessonid" value="' + str(lessonreply.lessonid.lessonid) + ' ">' + lessonreply.lessonid.lessonname + '</option>'
    
    temp = ''

    for lesson in lessons: 
        if edit == True and change == False:
            if lesson.lessonid!=lessonreply.lessonid.lessonid:
                    temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        else:
            temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)