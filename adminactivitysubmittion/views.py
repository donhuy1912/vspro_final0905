from django.shortcuts import render, redirect
from homepage.models import ActivitySubmittion, Activity, Account, Chapter, Lesson, Item, Subject,UserDetail
from datetime import datetime
from homepage.myfunction import tokenFile
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittions = ActivitySubmittion.objects.all()
            for activitysubmittion in activitysubmittions:
                activitysubmittion.createdate = activitysubmittion.createdate
                activitysubmittion.editdate = activitysubmittion.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'activitysubmittions': activitysubmittions}
            return render(request, 'adminactivitysubmittion/activitysubmittion_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                # try:
                #     token_link = request.FILES['link']
                # except:
                #     token_link = None
                # lin = ''
                # if token_link != None:
                #     lin = tokenFile(token_link)
                activitysubmittion = ActivitySubmittion( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        activityid = Activity.objects.get(activityid = request.POST['activityid']),
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        link=request.POST['link'],
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                activitysubmittion.save()
                return redirect('/adminactivitysubmittion/')
            else:
                activitys = Activity.objects.all()
                for activity in activitys:
                    activity.createdate = activity.createdate
                    activity.editdate = activity.editdate
                
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
                    'activitys': activitys,
                }
                
            return render(request, 'adminactivitysubmittion/activitysubmittion_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittion = ActivitySubmittion.objects.get(activitysubmittionid=id)
            # activitysubmittion.link = activitysubmittion.link
            activitysubmittion.createdate = activitysubmittion.createdate
            activitysubmittion.editdate = datetime.now()
            accounts = Account.objects.all()
            subjects = Subject.objects.all()
            subjectid = activitysubmittion.activityid.itemid.lessonid.chapterid.subjectid
                
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate

            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate

            activitys = Activity.objects.all()
            for activity in activitys:
                activity.createdate = activity.createdate
                activity.editdate = activity.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'activitysubmittion': activitysubmittion,
                'activitys': activitys,
                'accounts': accounts,
                'subjects': subjects,
                'subjectid': subjectid,
            }
            return render(request, 'adminactivitysubmittion/activitysubmittion_edit.html', context)
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
            activitysubmittion = ActivitySubmittion.objects.filter(activitysubmittionid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            activitysubmittion = ActivitySubmittion.objects.filter(activitysubmittionid = id).update(activityid = Activity.objects.get(activityid = getNum(request.POST['activityid'])))
            activitysubmittion = ActivitySubmittion.objects.get(activitysubmittionid=id)
            activitysubmittion.createdate=activitysubmittion.createdate
            activitysubmittion.editdate=datetime.now()
            activitysubmittion.description=request.POST['description']
            activitysubmittion.content=request.POST['content']
            activitysubmittion.link=request.POST['link']
            activitysubmittion.isenable=request.POST['isenable']
            activitysubmittion.note=request.POST['note']
            activitysubmittion.save()
            return redirect('/adminactivitysubmittion/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            activitysubmittion = ActivitySubmittion.objects.get(activitysubmittionid= id)
            activitysubmittion.delete()
            return redirect('/adminactivitysubmittion/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
def validate_subjectactivitysubmittion(request):
    subject = request.GET.get('subject', None)
    chapters = Chapter.objects.filter(subjectid=subject)
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True
        
    if edit == True:
        activitysubmittion  = ActivitySubmittion.objects.get(activitysubmittionid = request.GET.get('activitysubmittion', None))
    
    if edit == False or change == True:
        s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
    else:
        if change == False:
            s= ' <option type="text" name="chapterid" value="' + str(activitysubmittion.activityid.itemid.lessonid.chapterid.chapterid) + ' ">' + activitysubmittion.activityid.itemid.lessonid.chapterid.chaptername + '</option>'
    
    temp = ''

    for chapter in chapters: 
        if edit == True and change == False:
            if chapter.chapterid != activitysubmittion.activityid.itemid.lessonid.chapterid.chapterid:
                    temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        else:
            temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)

#lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
def validate_chapteractivitysubmittion(request):
    chapter = request.GET.get('chapter', None)
    lessons = Lesson.objects.filter(chapterid=chapter)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittion = ActivitySubmittion.objects.get(activitysubmittionid = request.GET.get('activitysubmittion', None))

    if edit == False or change == True:
        s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="lessonid" value="' + str(activitysubmittion.activityid.itemid.lessonid.lessonid) + ' ">' + activitysubmittion.activityid.itemid.lessonid.lessonname + '</option>'
    
    temp = ''

    for lesson in lessons: 
        if edit == True and change == False:
            if lesson.lessonid!=activitysubmittion.activityid.itemid.lessonid.lessonid:
                    temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        else:
            temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)


#lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của item
def validate_lessonactivitysubmittion(request):
    lesson = request.GET.get('lesson', None)
    items = Item.objects.filter(lessonid=lesson)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittion  = ActivitySubmittion.objects.get(activitysubmittionid = request.GET.get('activitysubmittion', None))

    if edit == False or change == True:
        s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="itemid" value="' + str(activitysubmittion.activityid.itemid.itemid) + ' ">' + activitysubmittion.activityid.itemid.itemname + '</option>'
    
    temp = ''

    for item in items: 
        if edit == True and change == False:
            if item.itemid!=activitysubmittion.activityid.itemid.itemid:
                    temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        else:
            temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)



#lấy giá trị item được nhập vào để giới hạn giá trị show ra của activity
def validate_itemactivitysubmittion(request):
    item = request.GET.get('item', None)
    activitys = Activity.objects.filter(itemid=item)
    
    edit = request.GET.get('edit', False)
    if edit == '1': 
        edit = True
    
    change = request.GET.get('change', False)
    if change == '1': 
        change = True

    if edit == True:
        activitysubmittion  = ActivitySubmittion.objects.get(activitysubmittionid = request.GET.get('activitysubmittion', None))

    if edit == False or change == True:
        s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
    else:
        s= ' <option type="text" name="activityid" value="' + str(activitysubmittion.activityid.activityid) + ' ">' + activitysubmittion.activityid.activityname + '</option>'
    
    temp = ''

    for activity in activitys: 
        if edit == True and change == False:
            if activity.activityid!=activitysubmittion.activityid.activityid:
                    temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        else:
            temp = ' <option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
        s = s+temp

    data = {
        'is_taken': s
    }

    return JsonResponse(data)