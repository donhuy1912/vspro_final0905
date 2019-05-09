from django.shortcuts import render, redirect
from homepage.models import ActivityReply, Enrollment, Activity, Lesson, Chapter, Item, Account, Subject,UserDetail
from datetime import datetime
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activityreplys = ActivityReply.objects.all()
            for activityreply in activityreplys:
                activityreply.createdate = activityreply.createdate
                activityreply.editdate = activityreply.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'activityreplys': activityreplys}
            return render(request, 'adminactivityreply/activityreply_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            
            
            if request.method == 'POST':
                activityreply = ActivityReply( 
                                        enrollmentid = Enrollment.objects.get(enrollmentid = request.POST['accountid']),
                                        activityid = Activity.objects.get(activityid = request.POST['activityid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        rate=request.POST['rate'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                activityreply.save()
                return redirect('/adminactivityreply/')
            else:
                activitys = Activity.objects.all()
                for activity in activitys:
                    activity.createdate = activity.createdate
                    activity.editdate = activity.editdate

                accounts = Account.objects.all()
                subjects = Subject.objects.all()
                enrollments = Enrollment.objects.all()
                
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
                    'accounts': accounts,
                    'subjects': subjects,
                    'activitys': activitys,
                    'enrollments': enrollments
                }
            
            return render(request, 'adminactivityreply/activityreply_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        acc = Account.objects.get(username = request.session['username'])
        if acc.accounttypeid.accounttypeid == 1:
            activityreply = ActivityReply.objects.get(activityreplyid=id)
            activityreply.createdate = activityreply.createdate
            activityreply.editdate = datetime.now()

            activitys = Activity.objects.all()
            for activity in activitys:
                activity.createdate = activity.createdate
                activity.editdate = activity.editdate

            accounts = Account.objects.all()
            enrollments = Enrollment.objects.all()
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

            userdetail=UserDetail.objects.get(accountid=acc)
            context = {
                'userdetail':userdetail,
                'acc':acc,
                'accounts': accounts,
                'subjects': subjects,
                'activityreply': activityreply,
                'activitys': activitys,
                'enrollments': enrollments,
            }

            return render(request, 'adminactivityreply/activityreply_edit.html', context)
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
            activityreply = ActivityReply.objects.filter(activityreplyid = id).update(enrollmentid = Enrollment.objects.get(enrollmentid = getNum(request.POST['accountid'])))
            activityreply = ActivityReply.objects.filter(activityreplyid = id).update(activityid = Activity.objects.get(activityid = getNum(request.POST['activityid'])))
            activityreply = ActivityReply.objects.get(activityreplyid=id)
            activityreply.createdate=activityreply.createdate
            activityreply.editdate=datetime.now()
            activityreply.content=request.POST['content']
            activityreply.rate=request.POST['rate']
            activityreply.isenable=request.POST['isenable']
            activityreply.note=request.POST['note']
            activityreply.save()
            return redirect('/adminactivityreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activityreply = ActivityReply.objects.get(activityreplyid= id)
            activityreply.delete()
            return redirect('/adminactivityreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
# def validate_subjectactivityreply(request):
#     subject = request.GET.get('subject',None)
#     chapters = Chapter.objects.filter(subjectid = subject)
#     s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
#     temp = ''
#     for chapter in chapters:
#         temp = '<option type="text" name="chapterid" value=" ' + str(chapter.chapterid) + ' "> ' + chapter.chaptername + ' </option>'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data)



def validate_subjectactivityreply(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
        
    if edit == True:
        activityreply  = ActivityReply.objects.get(activityreplyid = request.GET.get('activityreply', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="chapterid" value="' + str(activityreply.activityid.itemid.lessonid.chapterid.chapterid) + ' ">' + activityreply.activityid.itemid.lessonid.chapterid.chaptername + '</option>'
    
    temp = ''

    for chapter in chapters: 
        if edit == True and change == False:
            if chapter.chapterid != activityreply.activityid.itemid.lessonid.chapterid.chapterid:
                    temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        else:
            temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
# def validate_chapteractivityreply(request):
#     chapter = request.GET.get('chapter', None)
#     lessons = Lesson.objects.filter(chapterid = chapter)
#     s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
#     temp = ''
#     for lesson in lessons:
#         temp = '<option type="text" name="lessonid" value=" ' + str(lesson.lessonid) + ' "> ' + lesson.lessonname + ' </option>'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data) 


def validate_chapteractivityreply(request):
    chapter = request.GET.get('chapter', None)
    lessons = Lesson.objects.filter(chapterid=chapter)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activityreply = ActivityReply.objects.get(activityreplyid = request.GET.get('activityreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="lessonid" value="' + str(activityreply.activityid.itemid.lessonid.lessonid) + ' ">' + activityreply.activityid.itemid.lessonid.lessonname + '</option>'
    
    temp = ''

    for lesson in lessons: 
        if edit == True and change == False:
            if lesson.lessonid!=activityreply.activityid.itemid.lessonid.lessonid:
                    temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        else:
            temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của item
# def validate_lessonactivityreply(request):
#     lesson = request.GET.get('lesson',None)
#     items = Item.objects.filter(lessonid = lesson)
#     s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
#     temp = ''
#     for item in items:
#         temp = '<option type="text" name="itemid" value=" ' + str(item.itemid) + ' "> ' + item.itemname + ' </option>'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data)

def validate_lessonactivityreply(request):
    lesson = request.GET.get('lesson', None)
    items = Item.objects.filter(lessonid=lesson)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activityreply  = ActivityReply.objects.get(activityreplyid = request.GET.get('activityreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="itemid" value="' + str(activityreply.activityid.itemid.itemid) + ' ">' + activityreply.activityid.itemid.itemname + '</option>'
    
    temp = ''

    for item in items: 
        if edit == True and change == False:
            if item.itemid!=activityreply.activityid.itemid.itemid:
                    temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        else:
            temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)



#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
# def validate_itemactivityreply(request):
#     item = request.GET.get('item', None)
#     activitys = Activity.objects.filter(itemid = item)
#     s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
#     temp = ''
#     for activity in activitys:
#         temp = '<option type="text" name="activityid" value=" ' + str(activity.activityid) + ' "> ' + activity.activityname + ' </option>'
#         s+=temp
#     data = {
#         'is_taken': s
#     }
#     return JsonResponse(data) 


def validate_itemactivityreply(request):
    item = request.GET.get('item', None)
    activitys = Activity.objects.filter(itemid=item)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activityreply  = ActivityReply.objects.get(activityreplyid = request.GET.get('activityreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="activityid" value="' + str(activityreply.activityid.activityid) + ' ">' + activityreply.activityid.activityname + '</option>'
    
    temp = ''

    for activity in activitys: 
        if edit == True and change == False:
            if activity.activityid!=activityreply.activityid.activityid:
                    temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        else:
            temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)
