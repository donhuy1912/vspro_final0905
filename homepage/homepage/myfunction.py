from datetime import datetime
import re
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from homepage.models import *
import random
import hashlib
from homepage.myclass import *

# Hàm tách số khỏi chuỗi
def getNum(x):
	return int(''.join(ele for ele in x if ele.isdigit()))
	
# Hàm kiểm tra Account, Nếu có return True
def boolcheckAccount(userName, passWord):
    try:
        acc = Account.objects.get(username__iexact = userName, password = hashPassword(passWord))
    except Account.DoesNotExist:
        return None
    if acc is not None:
        return True
    return False

# Hàm tìm kiếm username đã có sẵn chưa. Nếu đã có trả về True
def boolcheckUser(userName):
    try:
        username = Account.objects.get(username=userName)
    except Account.DoesNotExist:
        return None
    if username is not None:
        return True
    return False

# Hàm check email. Nếu email hợp lệ return True
def isEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return True
    return False

# Hàm tìm kiếm email đã có sẵn chưa. Nếu đã có trả về True
def boolcheckEmail(email):
    try:
        email = UserDetail.objects.get(email=email)
    except UserDetail.DoesNotExist:
        return None
    if email is not None:
        return True
    return False

# Hàm check số điện thoại. Nếu sdt hợp lệ return True
def boolcheckphoneNumber(phone_number):
    if phone_number == '':
        return True
    elif len(phone_number) > 11 or len(phone_number) < 10:
	    return False
    elif phone_number[0] != '0':
	    return False
    else:
	    for i in range(len(phone_number)):
		    if not phone_number[i].isdigit():
			    return False
    return True

# Hàm kiểm tra password (dài hơn 7 ký tự, có chữ hoa, chữ thường và số.)
def boolcheckPassword(password):
    num = re.search(r'[0-9]', password) is None
    lowc = re.search(r'[a-z]', password) is None
    upc = re.search(r'[A-Z]', password) is None
    if len(password) < 8:
        return False
    elif (num or lowc or upc):
        return False
    return True

# Hàm kiểm tra khoảng trắng cho username và password
def boolcheckSpace(value):
    for i in range(len(value)):
        if value[i] == ' ':
            return True
    return False

# Hàm random 6 số sang chuỗi
def randomcode():
    strNum = str(random.randrange(100000,999999))
    return strNum
    
# Hàm lấy username (format: username + ' ' + code)
def getUsername(userandcode):
    s = ''
    for i in range(len(userandcode)):
	    if userandcode[i] != ' ':
		    s += userandcode[i]
	    else:
		    break
    return s

# Hàm hash password
def hashPassword(password):
	h = hashlib.md5(password.encode())
	s = h.hexdigest()
	return s

# Hàm kiểm tra có phải là số. Trả về True nếu là số.
def boolcheckInt(num):
    for i in range(len(num)):
        if not num[i].isdigit():
            return False
    return True
    
# Hàm lấy 5 môn học phổ biến theo id
# take second element for sort
def takeFirst(elem):
    return elem[0]
	
def top5subjects():
    subjects = Subject.objects.all()
    arr = []
    for sub in subjects:
        sub_id = sub.subjectid
        eroll_id = Enrollment.objects.filter(subjectid = sub_id)
        countEnroll= len(eroll_id)
        tup = (countEnroll, sub_id)
        arr.append(tuple(tup))
    arr_sorted = sorted(arr, key = takeFirst, reverse = True)
    num = len(arr_sorted)
    topNum = []
    if num < 5:
        for i in range(num):
            topNum.append(arr_sorted[i])
    else:
        for i in range(5):
            topNum.append(arr_sorted[i])
    arrsubjectId = [i[1] for i in topNum]
    return arrsubjectId

# Hàm lấy link avatar
def tokenFile(avatar):
    if avatar != None:
        fs = FileSystemStorage()
        avatar_name = fs.save(avatar.name, avatar)
        avatar_url = fs.url(avatar_name)
        return avatar_url
    return None

# Hàm tính rate 1 subject theo subject
def getrateSubject(subject):
    sumTime = 0
    countAR = 0
    avgRate = 0
    try:
        chapters = Chapter.objects.filter(subjectid = subject.subjectid)
        # Lấy id chapters
        chapid = []
        for chapter in chapters:
            chapid.append(chapter.chapterid)
        # Lấy lessons
        lessons = Lesson.objects.filter(chapterid__in = chapid)
        lessid = []
        for lesson in lessons:
            lessid.append(lesson.lessonid)
        # Lấy items
        items = Item.objects.filter(lessonid__in = lessid)
        iteid = []
        for item in items:
            iteid.append(item.itemid)
        # Lấy activities
        activities = Activity.objects.filter(itemid__in = iteid) 
        actid = []
        for activity in activities:
            actid.append(activity.activityid)
            sumTime += activity.time
        # Lấy activityReplys
        activityReplys = ActivityReply.objects.filter(activityid__in = actid)
        countAR = len(activityReplys)
        sumRate = 0
        for activityReply in activityReplys:
            sumRate += activityReply.rate
        if countAR > 0:
            avgRate = sumRate/countAR
        result = (round(avgRate,1), countAR, sumTime)
        return result
    except:
        result = (round(avgRate,1), countAR, sumTime)
        return result

# Hàm chuyển sang giờ phút: h..m
def converttimetoString(sumTime):
    if sumTime >= 60:
        mins = sumTime % 60
        hours = (sumTime - mins) / 60
        hours = int(hours)
        result = ' ' + str(hours) + 'h' + str(mins) + 'm'
        return result
  
    result = ' ' + str(sumTime) + 'm'
    return result

def converttimetoString2(sumTime):
    if sumTime >= 60:
        mins = sumTime % 60
        hours = (sumTime - mins) / 60
        hours = int(hours)
        result = str(hours) + ':' + str(mins) + ':00' 
        return result
  
    result = str(sumTime) + ':00' 
    return result
	
# Tính like subject
def getlikeSubjectId(subject):
    sublikes = SubjectLike.objects.filter(subjectid = subject.subjectid)
    return len(sublikes)

#Tính like forum
def getlikeForumId(forum):
    forlikes = ForumLike.objects.filter(forumtopicid = forum.forumtopicid)
    return len(forlikes)
	
# Hàm kiểm tra đăng kí khóa học chưa theo username
def checkenrollmentUser(subid, username):
    try:
        acc = Account.objects.get(username = username)
        enroll = Enrollment.objects.filter(subjectid = subid).filter(accountid = acc.accountid)
        if len(enroll) != 0:
            return True
        return False
    except:
        return False

# Hàm checklike
def checkLike(subid, username):
    try:
        acc= Account.objects.get(username=username)
        sublike = SubjectLike.objects.filter(subjectid = subid).filter(accountid = acc.accountid)
        if len(sublike) != 0:
            return True
        return False
    except:
        return False
		
# Hàm checklike Forum
def checkLikeForum(forid, username):
    try:
        acc= Account.objects.get(username=username)
        forlike = ForumLike.objects.filter(forumtopicid = forid).filter(accountid = acc.accountid)
        if len(forlike) != 0:
            return True
        return False
    except:
        return False

# Hàm lấy time theo chương
def gettimeChapter(chapter):
    sumTime = 0
    lessons = Lesson.objects.filter(chapterid = chapter.chapterid)
    lessid = []
    for lesson in lessons:
        lessid.append(lesson.lessonid)
    # Lấy items
    items = Item.objects.filter(lessonid__in = lessid)
    iteid = []
    for item in items:
        iteid.append(item.itemid)
    # Lấy activities
    activities = Activity.objects.filter(itemid__in = iteid) 
    actid = []
    for activity in activities:
        actid.append(activity.activityid)
        sumTime += activity.time

    return sumTime

# Hàm đếm lessons trong subject
def countLessonInSub(subject):
    chapters = Chapter.objects.filter(subjectid = subject.subjectid)
    # Lấy id chapters
    chapid = []
    for chapter in chapters:
        chapid.append(chapter.chapterid)
    # Lấy lessons
    lessons = Lesson.objects.filter(chapterid__in = chapid)
    return str(len(lessons)) + ' chủ đề'

# Hàm lấy rate trong activityreply
def getrateActivityDetail(subject):
    chapters = Chapter.objects.filter(subjectid = subject.subjectid)
    # Lấy id chapters
    chapid = []
    for chapter in chapters:
        chapid.append(chapter.chapterid)
    # Lấy lessons
    lessons = Lesson.objects.filter(chapterid__in = chapid)
    lessid = []
    for lesson in lessons:
        lessid.append(lesson.lessonid)
    # Lấy items
    items = Item.objects.filter(lessonid__in = lessid)
    iteid = []
    for item in items:
        iteid.append(item.itemid)
    # Lấy activities
    activities = Activity.objects.filter(itemid__in = iteid) 
    actid = []
    for activity in activities:
        actid.append(activity.activityid)
    # Lấy activityReplys
    activityReplys = ActivityReply.objects.filter(activityid__in = actid)
    
    s1 = s2 = s3 = s4 = s5 = 0
    p1 = p2 = p3 = p4 = p5 = 0
    s = 0
    for activityReply in activityReplys:
        if activityReply.rate == 1:
            s1 += 1
        elif activityReply.rate == 2:
            s2 += 1
        elif activityReply.rate == 3:
            s3 += 1
        elif activityReply.rate == 4:
            s4 += 1
        elif activityReply.rate == 5:
            s5 += 1
    s = s1 + s2 + s3 + s4 + s5
    sum = s1*1 + s2*2 + s3*3 + s4*4 + s5*5
    sumavg = 0
    if s != 0:
        p1 = round((s1/s)*100,0)
        p2 = round((s2/s)*100,0)
        p3 = round((s3/s)*100,0)
        p4 = round((s4/s)*100,0)
        p5 = round((s5/s)*100,0)
        sumavg = round(sum/s,1)
        
    result = rateStarDetail(s1,p1,s2,p2,s3,p3,s4,p4,s5,p5,s, sumavg)
    return result

# Hàm lấy 3 comment mới nhất
def getNewComment(subject):
    enrolls = Enrollment.objects.filter(subjectid=subject.subjectid)
    enrollid=[]
    for enroll in enrolls:
        enrollid.append(enroll.enrollmentid)
    activityReply = ActivityReply.objects.filter(enrollmentid__in=enrollid).order_by('-createdate')
    num = len(activityReply)
    if num > 3:
        results =activityReply[0:3]
    else:
        arrAR = []
        for i in range(0,num):
            arrAR.append(activityReply[i])
        results=arrAR
    newcmt=[]
    if len(results)!=0:
        for result in results:
            enroLL= Enrollment.objects.get(enrollmentid=result.enrollmentid.enrollmentid)
            acc=Account.objects.get(accountid=enroLL.accountid.accountid)
            temp=newestComment(acc.avatar,result.rate,acc.username,result.createdate,result.content)
            newcmt.append(temp)
    
    return newcmt

# Hàm lấy 5 giáo viên
def getFTeacher(subject):
    accMain = Account.objects.get(accountid = subject.accountid.accountid)
    subaccSide = SubjectTeacher.objects.filter(subjectid = subject)
    accSide = []
    accSide.append(accMain)
    for subacc in subaccSide:
        accSide.append(subacc.accountid)
    result = []
    for acc in accSide:
        teaDetail = UserDetail.objects.get(accountid = acc.accountid)
        fullname = teaDetail.lastname + " " + teaDetail.firstname
        temp = TeacherDetails(fullname, acc.avatar,acc)
        result.append(temp)
    num = len(result)
    if num > 5:
        result[0:5]
    else:
        result[0:num]

    return result

# Hàm check enrollment
def boolcheckEnroll(subject, userName):
    enroll = Enrollment.objects.filter(subjectid = subject)
    acc = Account.objects.get(username = userName)
    findEnroll = enroll.filter(accountid = acc)
    if len(findEnroll) != 0:
        return True
    return False

# Hàm lấy chương và danh sách lesson
def getChapterLessson(subject, account):
    chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
    result = []
    chaporder = 1
    enrollment = Enrollment.objects.filter(subjectid=subject).get(accountid=account)
    bfchap = 0
    for chapter in chapters:
        # KTra
        checkpass = ''
        if bfchap > 0:
            trackings = Tracking.objects.filter(chapterid = chapters[bfchap-1]).filter(enrollmentid = enrollment)
            divi = getCountActivityInChapter(chapters[bfchap-1])
            if divi != 0:
                percent=int(len(trackings)/divi*100)
            else:
                percent = 0
            if percent < 66:
                checkpass="pointer-events:none"
        bfchap +=1
        lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
        nameChap =  str(chaporder) + '. ' + chapter.chaptername 
        chaporder += 1
        # xử lý tên lesson
        lessorder = 1
        numChapid = chapter.chapterid
        chapter.chapterid = 'check' + '(' + str(chapter.chapterid) + ')' 
        for lesson in lessons:
            lesson.lessonname = str(chaporder-1)+'. ' + str(lessorder) + '. ' + lesson.lessonname
            lessorder += 1
        temp = ChapAndLess(chapter.chapterid, nameChap, lessons, numChapid, checkpass)
        result.append(temp)
        chapter.chapterid = numChapid
    
    return result
        
# Hàm lấy số trong chuỗi
def getNumInString(s):
    result = ''
    for i in s:
        if i.isdigit():
            result += i
    if result == '':
    	return None
    else:
    	return int(result)

# Hàm lấy item và danh sách hoạt động
def getItemActivity(lesson):
    items = Item.objects.filter(lessonid=lesson).order_by('order')
    result=[]
    itemorder =1
    activityorder =1
    for item in items:
        activityorder = 1
        activities = Activity.objects.filter(itemid=item).order_by('order')
        item.itemname =item.itemname
        for activity in activities:
            activity.activityname=  str(activityorder)+'. '+ activity.activityname
            activityorder +=1
        temp=ItemAndActivity(item,activities)
        result.append(temp)
        itemorder+=1
    return result

# Hàm kiểm tra hđong nguoi học
def boolcheckActivityTracking(activity, account):
    enrollments = Enrollment.objects.filter(accountid = account)
    item = activity.itemid
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject = chapter.subjectid
    enrollment = enrollments.get(subjectid = subject.subjectid)
    try:
        tracking = Tracking.objects.filter(enrollmentid = enrollment).get(activityid = activity)
    except:
        return 0
    if tracking != None and tracking.isenable == 1:
        return 1
    return 0

# Hàm get name pdf
def getNamePDF(link):
    result = link.replace("/media/","")
    result = result.replace(".pdf","")
    return result

# Hàm check đã học chương ==> true
def boolcheckChapterProcess(chapter, account):
    subject = chapter.subjectid
    enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject)
    track = Tracking.objects.filter(enrollmentid = enrollment).filter(chapterid = chapter)
    if (len(track) > 0):
        return True
    return False

# Hàm process chapter
def getProcessChapter(subject, account):
    chapters = Chapter.objects.filter(subjectid = subject).order_by('order')

    listchapter = []
    i = 1
    for chapter in chapters:
        iscom = boolcheckChapterProcess(chapter, account)
        if iscom:
            done = 'selected'
        else:
            done = 'disabled'
        temp = ChapterProcess(i, chapter, done)
        i += 1
        listchapter.append(temp)

    return listchapter

# Hàm check đã học bài ==> true
def boolcheckActivityProcess(activity, account):
    item = activity.itemid
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject = chapter.subjectid

    enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject)
    track = Tracking.objects.filter(enrollmentid = enrollment).filter(activityid = activity)
    if (len(track) > 0):
        return True
    return False

# # Hàm check đã hoàn thành course (subject)
# def boolcheckSubjectProcess(subject, account):
#     # print(subject.chapterid)
#     enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject.subjectid)
#     chapters = Chapter.objects.filter(subjectid = subject.subjectid)
#     for chapter in chapters:
#         lessons = Lesson.objects.filter(chapterid = chapter.chapterid)
#         for lesson in lessons:
#             items = Item.objects.filter(lessonid = lesson.lessonid)
#             for item in items:
#                 activitys = Activity.objects.filter(itemid = item.itemid)
#                 for activity in activitys:
#                     if boolcheckActivityProcess(activity, account) == False:
#                         return False

#     return True
	
# Hàm process activity
def getProcessActivity(activity, account):
    item = activity.itemid
    activities = Activity.objects.filter(itemid = item).order_by('order')

    listactivity = []
    i = 1
    for activity in activities:
        iscom = boolcheckActivityProcess(activity, account)
        if iscom:
            done = 'selected'
        else:
            done = 'disabled'
        temp = ActivityProcess(i, activity, done)
        i += 1
        listactivity.append(temp)

    return listactivity

# Hàm embed link youtube
def getEmbedYoutube(link):
    strSpecial = 'watch?v='
    emb = 'embed/'
    embedlink = link.replace(strSpecial, emb)
    s = ''
    for i in range(0,len(embedlink)):
        if embedlink[i] == '&':
            break
        else:
            s += embedlink[i]
    return s

# Hàm check GV được phân quyền chỉnh sửa
def boolcheckTeacherPermit(acccount, subject):
    accTeacher = subject.accountid
    subTeachers = SubjectTeacher.objects.filter(subjectid = subject)
    accT = []
    accT.append(accTeacher)
    for subTeacher in subTeachers:
        accT.append(subTeacher.accountid)
    for acc in accT:
        if (acccount.accountid == acc.accountid):
            return True
    return False
    
# Lấy Hd gần nhất trong 1 môn của một người học:
def getActivityMaxInSub(enrollment):
    trackings = Tracking.objects.filter(enrollmentid=enrollment).filter(subjectid = enrollment.subjectid).order_by('-trackingid')
    if len(trackings) == 0:
        return 0
    else:
        act = trackings[0].activityid
        return act

# Hàm lấy số lượng activity trong 1 subject
def getCountActivity(subject):
    try:
        chapters = Chapter.objects.filter(subjectid = subject.subjectid)
        # Lấy id chapters
        chapid = []
        for chapter in chapters:
            chapid.append(chapter.chapterid)
        # Lấy lessons
        lessons = Lesson.objects.filter(chapterid__in = chapid)
        lessid = []
        for lesson in lessons:
            lessid.append(lesson.lessonid)
        # Lấy items
        items = Item.objects.filter(lessonid__in = lessid)
        iteid = []
        for item in items:
            iteid.append(item.itemid)
        # Lấy activities
        activities = Activity.objects.filter(itemid__in = iteid) 
        return len(activities)
    except:
        return 0

# hàm tính số act trong 1 chương
def getCountActivityInChapter(chapter):
    try:
        # Lấy lessons
        lessons = Lesson.objects.filter(chapterid = chapter)
        lessid = []
        for lesson in lessons:
            lessid.append(lesson.lessonid)
        # Lấy items
        items = Item.objects.filter(lessonid__in = lessid)
        iteid = []
        for item in items:
            iteid.append(item.itemid)
        # Lấy activities
        activities = Activity.objects.filter(itemid__in = iteid) 
        return len(activities)
    except:
        return 0

# hàm tính số act trong 1 lesson
def getActivityInLesson(lesson):
    items = Item.objects.filter(lessonid = lesson).order_by('order')
    arrAct = []
    for item in items:
        activities = Activity.objects.filter(itemid= item).order_by('order')
        for activity in activities:
            arrAct.append(activity)
    return arrAct
def getActivitySUBInLesson(lesson):
    items = Item.objects.filter(lessonid = lesson).order_by('order')
    arrAct = []
    for item in items:
        activities = Activity.objects.filter(itemid= item).filter(activitytypeid=6).order_by('order')
        for activity in activities:
            arrAct.append(activity)
    return arrAct
#hàm lấy level :
def getLevel(exp):
    sum =exp
    level=1
    expeachlevel=100
    while exp > expeachlevel:
        exp=exp-expeachlevel
        level+=1
        expeachlevel=expeachlevel*1.25
    expperleft= int(exp/expeachlevel*100)
    result= Level(level,sum,expperleft)
    return result

# Hàm  get rank
def getRank(level):
    rankc=int(level/5)
    name=''
    ava=''
    if rankc == 0:
        name ='Nông Dân Sơ Cấp'
        ava='/media/rank/chevron-0.png'
    elif rankc == 1:
        name = 'Nông Dân Trung Cấp'
        ava='/media/rank/chevron-1.png'
    elif rankc == 2:
        name = 'Nông Dân Cao Cấp'
        ava='/media/rank/chevron-2.png'
    elif rankc == 3:
        name = 'Binh sĩ Sơ Cấp'
        ava='/media/rank/chevron-3.png'
    elif rankc == 5:
        name = 'Binh Sĩ Trung Cấp'
        ava='/media/rank/chevron-4.png'
    elif rankc == 7:
        name = 'Binh Sĩ Cao Cấp'
        ava='/media/rank/chevron-5.png'
    elif rankc == 9:
        name = 'Đặc Công Sơ Cấp'
        ava='/media/rank/chevron-7.png'
    elif rankc == 11:
        name = 'Đặc Công Trung Cấp'
        ava='/media/rank/chevron-8.png'
    elif rankc == 13:
        name = 'Đặc Công Cao Cấp'
        ava='/media/rank/chevron-9.png'
    elif rankc == 15:
        name = 'Cấm Quân Sơ Cấp'
        ava='/media/rank/chevron-13.png'
    elif rankc == 17:
        name = 'Cấm Quân Trung Cấp'
        ava='/media/rank/chevron-14.png'
    elif rankc == 19:
        name = 'Cấm Quân Cao Cấp'
        ava='/media/rank/chevron-15.png'
    elif rankc == 21:
        name = 'Hiệp Sĩ Hoàng Gia Sơ Cấp'
        ava='/media/rank/chevron-16.png'
    elif rankc == 24:
        name = 'Hiệp Sĩ Hoàng Gia Trung Cấp'
        ava='/media/rank/chevron-17.png'
    elif rankc == 27:
        name = 'Hiệp Sĩ Hoàng Gia Cao Cấp'
        ava='/media/rank/chevron-18.png'
    elif rankc == 30:
        name = 'Hoàng Tộc Sơ Cấp'
        ava='/media/rank/chevron-19.png'
    elif rankc == 35:
        name = 'Hoàng Tộc Cao Cấp'
        ava='/media/rank/chevron-20.png'
    elif rankc == 40:
        name = 'Vua'
        ava='/media/rank/chevron-21.png'

    return Rank(ava,name)

# hàm ktra Khi Load có link act thuộc chương chưa mở khóa
def boolcheckUnlockChapter(chapter, account, sesslook):
    subject = chapter.subjectid
    enrollment = Enrollment.objects.filter(subjectid = subject).get(accountid = account)
    pos=0
    chapters=Chapter.objects.filter(subjectid=subject).order_by("order")
    if sesslook != 0:
        return True
    else:
        if chapter.chapterid == chapters[0].chapterid:
            return True
        for chap in chapters:
            pos+=1
            if chap.chapterid == chapter.chapterid :
                break
        chapbf =chapters[pos-1]
        trackings = Tracking.objects.filter(chapterid = chapbf)
        div = getCountActivityInChapter(chapbf)
        if div != 0:
            percent = int(len(trackings)/div*100)
        else:
            return False
        if percent > 66:
            return True
        return False

# Hàm check đã hoàn thành course (subject)
def boolcheckSubjectProcess(subject, account):
    enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject.subjectid)
    chapters = Chapter.objects.filter(subjectid = subject.subjectid)
    for chapter in chapters:
        lessons = Lesson.objects.filter(chapterid = chapter.chapterid)
        for lesson in lessons:
            items = Item.objects.filter(lessonid = lesson.lessonid)
            for item in items:
                activitys = Activity.objects.filter(itemid = item.itemid)
                for activity in activitys:
                    if boolcheckActivityProcess(activity, account) == False:
                        return False

    return True

# Hàm xóa 1 activity
def delActivity(activity):
    item = activity.itemid
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject = chapter.subjectid
    # Lấy hoạt động trong lesson
    activities = getActivityInLesson(lesson)
    # tìm HD có HD req là HD muốn xóa. Set HD ràng buộc về NULL
    for act in activities:
        if act.requiredactivityid == activity: 
            act.requiredactivityid = None
            act.save()      
    # Lấy vị trí activity cần xóa => sort
    numorder = activity.order
    # Xoá list Activityreply
    actReps = ActivityReply.objects.filter(activityid = activity)
    for actRep in actReps:
        actRep.delete()
    # Xóa list Activity Submition , xóa actSubRep
    actSubmits = ActivitySubmittion.objects.filter(activityid= activity)
    for actSubmit in actSubmits:
        actSubReps = ActivitySubmittionReply.objects.filter(activitysubmittionid=actSubmit)
        for actSubRep in actSubReps:
            actSubRep.delete()
        actSubmit.delete()
    # Tracking
    trackings = Tracking.objects.filter(activityid = activity)
    for tracking in trackings:
        tracking.delete()
    # Xóa
    activity.delete()
    # Sort act
    acts = Activity.objects.filter(itemid = item).order_by('order')
    for act in acts:
        if act.order > numorder:
            act.order = act.order-1
            act.save()









