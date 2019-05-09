from django.shortcuts import render, redirect
from homepage.models import ActivitySubmittionReply,UserDetail, Enrollment, ActivitySubmittion, Chapter, Lesson, Item, Activity, Subject, Account
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittionreplys = ActivitySubmittionReply.objects.all()
            for activitysubmittionreply in activitysubmittionreplys:
                activitysubmittionreply.createdate = activitysubmittionreply.createdate
                activitysubmittionreply.editdate = activitysubmittionreply.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,'activitysubmittionreplys': activitysubmittionreplys}
            return render(request, 'adminactivitysubmittionreply/activitysubmittionreply_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                activitysubmittionreply = ActivitySubmittionReply( 
                                        enrollmentid = Enrollment.objects.get(enrollmentid = request.POST['accountid']),
                                        activitysubmittionid = ActivitySubmittion.objects.get(activitysubmittionid = request.POST['activitysubmittionid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        content=request.POST['content'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                activitysubmittionreply.save()
                return redirect('/adminactivitysubmittionreply/')
            else:
                activitysubmittions = ActivitySubmittion.objects.all()
                for activitysubmittion in activitysubmittions:
                    activitysubmittion.createdate = activitysubmittion.createdate
                    activitysubmittion.editdate = activitysubmittion.editdate
                
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
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts,
                    'subjects': subjects,
                    'activitysubmittions': activitysubmittions,
                    'enrollments': enrollments,
                }
                
            return render(request, 'adminactivitysubmittionreply/activitysubmittionreply_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittionreply = ActivitySubmittionReply.objects.get(activitysubmittionreplyid=id)
            activitysubmittionreply.createdate = activitysubmittionreply.createdate
            activitysubmittionreply.editdate = datetime.now()

            activitysubmittions = ActivitySubmittion.objects.all()
            for activitysubmittion in activitysubmittions:
                activitysubmittion.createdate = activitysubmittion.createdate
                activitysubmittion.editdate = activitysubmittion.editdate
            
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
                'activitysubmittionreply': activitysubmittionreply,
                'activitysubmittions': activitysubmittions,
                'enrollments': enrollments
            }

            return render(request, 'adminactivitysubmittionreply/activitysubmittionreply_edit.html', context)
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
            activitysubmittionreply = ActivitySubmittionReply.objects.filter(activitysubmittionreplyid = id).update(enrollmentid = Enrollment.objects.get(enrollmentid = getNum(request.POST['accountid'])))
            activitysubmittionreply = ActivitySubmittionReply.objects.filter(activitysubmittionreplyid = id).update(activitysubmittionid = ActivitySubmittion.objects.get(activitysubmittionid = getNum(request.POST['submittionid'])))
            activitysubmittionreply = ActivitySubmittionReply.objects.get(activitysubmittionreplyid=id)
            activitysubmittionreply.createdate=activitysubmittionreply.createdate
            activitysubmittionreply.editdate=datetime.now()
            activitysubmittionreply.content=request.POST['content']
            activitysubmittionreply.isenable=request.POST['isenable']
            activitysubmittionreply.note=request.POST['note']
            activitysubmittionreply.save()
            return redirect('/adminactivitysubmittionreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittionreply = ActivitySubmittionReply.objects.get(activitysubmittionreplyid= id)
            activitysubmittionreply.delete()
            return redirect('/adminactivitysubmittionreply/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
def validate_subjectactivitysubmittionreply(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
        
    if edit == True:
        activitysubmittionreply  = ActivitySubmittionReply.objects.get(activitysubmittionreplyid = request.GET.get('activitysubmittionreply', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="chapterid" value="' + str(activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.chapterid.chapterid) + ' ">' + activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.chapterid.chaptername + '</option>'
    
    temp = ''

    for chapter in chapters: 
        if edit == True and change == False:
            if chapter.chapterid != activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.chapterid.chapterid:
                    temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        else:
            temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
def validate_chapteractivitysubmittionreply(request):
    chapter = request.GET.get('chapter', None)
    lessons = Lesson.objects.filter(chapterid=chapter)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittionreply = ActivitySubmittionReply.objects.get(activitysubmittionreplyid = request.GET.get('activitysubmittionreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="lessonid" value="' + str(activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.lessonid) + ' ">' + activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.lessonname + '</option>'
    
    temp = ''

    for lesson in lessons: 
        if edit == True and change == False:
            if lesson.lessonid!=activitysubmittionreply.activitysubmittionid.activityid.itemid.lessonid.lessonid:
                    temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        else:
            temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của item
def validate_lessonactivitysubmittionreply(request):
    lesson = request.GET.get('lesson', None)
    items = Item.objects.filter(lessonid=lesson)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittionreply  = ActivitySubmittionReply.objects.get(activitysubmittionreplyid = request.GET.get('activitysubmittionreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="itemid" value="' + str(activitysubmittionreply.activitysubmittionid.activityid.itemid.itemid) + ' ">' + activitysubmittionreply.activitysubmittionid.activityid.itemid.itemname + '</option>'
    
    temp = ''

    for item in items: 
        if edit == True and change == False:
            if item.itemid!=activitysubmittionreply.activitysubmittionid.activityid.itemid.itemid:
                    temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        else:
            temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị item được nhập vào để giới hạn giá trị show ra của activity
def validate_itemactivitysubmittionreply(request):
    item = request.GET.get('item', None)
    activitys = Activity.objects.filter(itemid=item)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittionreply  = ActivitySubmittionReply.objects.get(activitysubmittionreplyid = request.GET.get('activitysubmittionreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="activityid" value="' + str(activitysubmittionreply.activitysubmittionid.activityid.activityid) + ' ">' + activitysubmittionreply.activitysubmittionid.activityid.activityname + '</option>'
    
    temp = ''

    for activity in activitys: 
        if edit == True and change == False:
            if activity.activityid!=activitysubmittionreply.activitysubmittionid.activityid.activityid:
                    temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        else:
            temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị activity được nhập vào để giới hạn giá trị show ra của activitysubmittion
def validate_activityactivitysubmittionreply(request):
    activity = request.GET.get('activity', None)
    activitysubmittions = ActivitySubmittion.objects.filter(activityid=activity)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittionreply  = ActivitySubmittionReply.objects.get(activitysubmittionreplyid = request.GET.get('activitysubmittionreply', None))

    if edit == False or change == True:
        s = '<option type="text" name="activitysubmittionid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="activitysubmittionid" value="' + str(activitysubmittionreply.activitysubmittionid.activitysubmittionid) + ' ">' + activitysubmittionreply.activitysubmittionid.description + '</option>'
    
    temp = ''

    for activitysubmittion in activitysubmittions: 
        if edit == True and change == False:
            if activitysubmittion.activitysubmittionid!=activitysubmittionreply.activitysubmittionid.activitysubmittionid:
                    temp = ' <option type="text" name="activitysubmittionid" value="' + str(activitysubmittion.activitysubmittionid) + ' ">' + activitysubmittion.description + '</option>'
        else:
            temp = ' <option type="text" name="activitysubmittionid" value="' + str(activitysubmittion.activitysubmittionid) + ' ">' + activitysubmittion.description + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)
