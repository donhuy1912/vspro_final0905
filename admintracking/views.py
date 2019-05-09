from django.shortcuts import render, redirect
from homepage.models import UserDetail, Tracking, Enrollment, Subject, SubjectPart, Chapter, Lesson, Item, Activity, Account
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            trackings = Tracking.objects.all()
            for tracking in trackings:
                tracking.createdate = tracking.createdate
                tracking.editdate = tracking.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'trackings': trackings}
            return render(request, 'admintracking/tracking_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                tracking = Tracking( 
                                        enrollmentid = Enrollment.objects.get(enrollmentid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        subjectpartid = SubjectPart.objects.get(subjectpartid = request.POST['subjectpartid']),
                                        chapterid = Chapter.objects.get(chapterid = request.POST['chapterid']),
                                        lessonid = Lesson.objects.get(lessonid = request.POST['lessonid']),
                                        itemid = Item.objects.get(itemid = request.POST['itemid']),
                                        activityid = Activity.objects.get(activityid = request.POST['activityid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                tracking.save()
                return redirect('/admintracking/')
            else:
                subjectparts = SubjectPart.objects.all()
                accounts = Account.objects.all()
                enrollments = Enrollment.objects.all()
                subjects = Subject.objects.all()
                chapters = Chapter.objects.all()
                lessons = Lesson.objects.all()
                items = Item.objects.all()
                activitys = Activity.objects.all()

                for subjectpart in subjectparts:
                    subjectpart.createdate = subjectpart.createdate
                    subjectpart.editdate = subjectpart.editdate
                
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate

                for enrollment in enrollments:
                    enrollment.createdate = enrollment.createdate
                    enrollment.editdate = enrollment.editdate
                
                for subject in subjects:
                    subject.createdate = subject.createdate
                    subject.editdate = subject.editdate

                for chapter in chapters:
                    chapter.createdate = chapter.createdate
                    chapter.editdate = chapter.editdate

                for lesson in lessons:
                    lesson.createdate = lesson.createdate
                    lesson.editdate = lesson.editdate
                
                for item in items:
                    item.createdate = item.createdate
                    item.editdate = item.editdate

                for activity in activitys:
                    activity.createdate = activity.createdate
                    activity.editdate = activity.editdate
                
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'subjectparts':subjectparts,
                    'accounts':accounts,
                    'enrollments':enrollments,
                    'subjects':subjects,
                    'chapters':chapters,
                    'lessons':lessons,
                    'items':items,
                    'activitys':activitys,
                }

            return render(request, 'admintracking/tracking_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            tracking = Tracking.objects.get(trackingid=id)
            tracking.createdate = tracking.createdate
            tracking.editdate = datetime.now()

            subjectparts = SubjectPart.objects.all()
            accounts = Account.objects.all()
            enrollments = Enrollment.objects.all()
            subjects = Subject.objects.all()
            chapters = Chapter.objects.all()
            lessons = Lesson.objects.all()
            items = Item.objects.all()
            activitys = Activity.objects.all()

            for subjectpart in subjectparts:
                subjectpart.createdate = subjectpart.createdate
                subjectpart.editdate = subjectpart.editdate
            
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            for enrollment in enrollments:
                enrollment.createdate = enrollment.createdate
                enrollment.editdate = enrollment.editdate
            
            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate

            for chapter in chapters:
                chapter.createdate = chapter.createdate
                chapter.editdate = chapter.editdate

            for lesson in lessons:
                lesson.createdate = lesson.createdate
                lesson.editdate = lesson.editdate
                
            for item in items:
                item.createdate = item.createdate
                item.editdate = item.editdate

            for activity in activitys:
                activity.createdate = activity.createdate
                activity.editdate = activity.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'tracking': tracking,
                'subjectparts':subjectparts,
                'accounts':accounts,
                'enrollments':enrollments,
                'subjects':subjects,
                'chapters':chapters,
                'lessons':lessons,
                'items':items,
                'activitys':activitys,
            }
            return render(request, 'admintracking/tracking_edit.html', context)
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
            tracking = Tracking.objects.filter(trackingid = id).update(enrollmentid = Enrollment.objects.get(enrollmentid = getNum(request.POST['accountid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(subjectid = Subject.objects.get(subjectid = getNum(request.POST['subjectid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(subjectpartid = SubjectPart.objects.get(subjectpartid = getNum(request.POST['subjectpartid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(chapterid = Chapter.objects.get(chapterid = getNum(request.POST['chapterid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(lessonid = Lesson.objects.get(lessonid = getNum(request.POST['lessonid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(itemid = Item.objects.get(itemid = getNum(request.POST['itemid'])))
            tracking = Tracking.objects.filter(trackingid = id).update(activityid = Activity.objects.get(activityid = getNum(request.POST['activityid'])))
            tracking = Tracking.objects.get(trackingid=id)
            tracking.createdate=tracking.createdate
            tracking.editdate=datetime.now()
            tracking.isenable=request.POST['isenable']
            tracking.note=request.POST['note']
            tracking.save()
            return redirect('/admintracking/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            tracking = Tracking.objects.get(trackingid= id)
            tracking.delete()
            return redirect('/tables_relationship/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
def validate_subjecttracking(request):
    subject = request.GET.get('subject',None)
    chapters = Chapter.objects.filter(subjectid = subject)
    s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    temp = ''
    for chapter in chapters:
        temp = '<option type="text" name="chapterid" value=" ' + str(chapter.chapterid) + ' "> ' + chapter.chaptername + ' </option>'
        s+=temp
    data = {
        'is_taken': s
    }
    return JsonResponse(data)


#lấy giá trị activity được nhập vào để giới hạn giá trị show ra của activitysubmittion
def validate_subjectparttracking(request):
    subject = request.GET.get('subject', None)
    subjectparts = SubjectPart.objects.filter(subjectid = subject)
    s = '<option type="text" name="subjectpartid" value="">-- Chọn --</option>'
    temp = ''
    for subjectpart in subjectparts:
        temp = '<option type="text" name="subjectpartid" value=" ' + str(subjectpart.subjectpartid) + ' "> ' + subjectpart.subjectpartname + ' </option>'
        s+=temp
    data = {
        'is_taken': s
    }
    return JsonResponse(data)


#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
def validate_chaptertracking(request):
    chapter = request.GET.get('chapter', None)
    lessons = Lesson.objects.filter(chapterid = chapter)
    s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
    temp = ''
    for lesson in lessons:
        temp = '<option type="text" name="lessonid" value=" ' + str(lesson.lessonid) + ' "> ' + lesson.lessonname + ' </option>'
        s+=temp
    data = {
        'is_taken': s
    }
    return JsonResponse(data) 


#lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của item
def validate_lessontracking(request):
    lesson = request.GET.get('lesson',None)
    items = Item.objects.filter(lessonid = lesson)
    s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
    temp = ''
    for item in items:
        temp = '<option type="text" name="itemid" value=" ' + str(item.itemid) + ' "> ' + item.itemname + ' </option>'
        s+=temp
    data = {
        'is_taken': s
    }
    return JsonResponse(data)


#lấy giá trị item được nhập vào để giới hạn giá trị show ra của activity
def validate_itemtracking(request):
    item = request.GET.get('item', None)
    activitys = Activity.objects.filter(itemid = item)
    s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
    temp = ''
    for activity in activitys:
        temp = '<option type="text" name="activityid" value=" ' + str(activity.activityid) + ' "> ' + activity.activityname + ' </option>'
        s+=temp
    data = {
        'is_taken': s
    }
    return JsonResponse(data)


