from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myfunction import *
from datetime import datetime
from homepage.myclass import *
from django.http import HttpResponse
from zipfile import ZipFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

# Create your views here.
def coursedetail(request, id):
    subject = Subject.objects.get(subjectid = id)
    button = 0 # chưa đăng nhập
    like = 0
    likeCount = getlikeSubjectId(subject)
    # load thống kê subject
    arrTimeName = []
    chapters = Chapter.objects.filter(subjectid = id).order_by("order")
    chaporder = 1
    for chap in chapters:
        chapfullname = "BÀI " + str(chaporder) + ' : ' + chap.chaptername
        temp = TimeNameChapter(chapfullname, gettimeChapter(chap), converttimetoString2(gettimeChapter(chap)))
        chaporder += 1
        arrTimeName.append(temp)
    timeSubject = 0
    for i in range(len(arrTimeName)):
        timeSubject += int(arrTimeName[i].time)
   
    timeSubject1 = converttimetoString(timeSubject)
    timeSubject2 = converttimetoString2(timeSubject)
    countEnroll = len(Enrollment.objects.filter(subjectid = id))
    createDate = subject.createdate.date()
    countlesson = countLessonInSub(subject)

    # Rate Details
    rateDetail = getrateActivityDetail(subject)
    # Get comment
    newcmt=getNewComment(subject)
    # Lấy 5 GV
    teachers = getFTeacher(subject)

    # SL chu de
    numChapter = len(chapters)

    if request.session.has_key('username'):
        # Lấy account user
        usename = request.session['username']
        account = Account.objects.get(username = usename)
        if checkLike(id, usename):
            like = 1

        if checkenrollmentUser(id, account.username):
            button = 1 
        else:
            button = 2 # đăng nhập chưa đăng kí
        
        context = {
            'subject':subject,
            'account':account,
            'button':button,
            'like':like,
            'likeCount':likeCount,
            'arrTimeName': arrTimeName,
            'timeSubject1':timeSubject1,
            'timeSubject2':timeSubject2,
            'countEnroll':countEnroll,
            'createDate':createDate,
            'countlesson':countlesson,
            'rateDetail':rateDetail,
            'newcmt':newcmt,
            'teachers':teachers,
            'numChapter':numChapter,
        }
    else:
        context = {
            'subject':subject,
            'button':button,
            'like':like,
            'likeCount':likeCount,
            'arrTimeName': arrTimeName,
            'timeSubject1':timeSubject1,
            'timeSubject2':timeSubject2,
            'countEnroll':countEnroll,
            'createDate':createDate,
            'countlesson':countlesson,
            'rateDetail':rateDetail,
            'newcmt':newcmt,
            'teachers':teachers,
            'numChapter':numChapter,
        }

    return render(request, 'course/coursedetail.html', context )

def enroll(request, id):
    subject = Subject.objects.get(subjectid = id)
    if request.session.has_key('username'):
        username = request.session['username']
        account = Account.objects.get(username=username)
        
        enrollment = Enrollment(
                            accountid = Account.objects.get(accountid = account.accountid),
                            subjectid = subject,
                            createdate= datetime.now(), 
                            editdate= datetime.now(),
                            isenable = 1,  
        )
        enrollment.save()

    return redirect('course:coursedetail', id = subject.subjectid)

def coursepart(request, id):
    subject= Subject.objects.get(subjectid=id)

    if request.session.has_key('username') and subject.isenable==1 :
        account = Account.objects.get(username=request.session['username'])
        if boolcheckEnroll(subject, request.session['username']):
            subject = Subject.objects.get(subjectid = id)
            subpart1 = SubjectPart.objects.filter(subjectid = subject).get(order = 1)
            subpart2 = SubjectPart.objects.filter(subjectid = subject).get(order = 2)
            subpart3 = SubjectPart.objects.filter(subjectid = subject).get(order = 3)
            subpart4 = SubjectPart.objects.filter(subjectid = subject).get(order = 4)
            subpartDetail = getrateSubject(subject)
            avgRate = subpartDetail[0]
            countAR = subpartDetail[1]
            sumTime = subpartDetail[2]
            sublikes = getlikeSubjectId(subject) 
            subpartdetail = SubPartDetail(avgRate, countAR, converttimetoString(sumTime), sublikes)
            # part game
            listgame = Game.objects.filter(subjectid=subject.subjectid)
            countgame = len(listgame)
            grate = 0
            for ga in listgame:
                listrate = GameRate.objects.filter(gameid = ga)
                countrate = 0
                for rate in listrate:
                    countrate += rate.rate
                numlistrate = len(listrate)
                if numlistrate > 0:
                    grate = countrate/numlistrate

            countforum = len(Forum.objects.filter(subjectid=subject.subjectid))
            countprojectshare = len(ProjectShare.objects.filter(enviromentcateid=subject.enviromentcateid))

            context = {
                'account':account,
                'subject':subject,
                'subpart1':subpart1,
                'subpart2':subpart2,
                'subpart3':subpart3,
                'subpart4':subpart4,
                'subpartdetail':subpartdetail,
                'countgame':countgame,
                'grate': grate,
                'countforum':countforum,
                'countprojectshare':countprojectshare,
            }
            return render(request,'course/coursepart.html', context)
        else:
            return redirect('course:coursedetail', id=subject.subjectid)
        
    else:
        return redirect('course:coursedetail', id=subject.subjectid)
    
def coursechapter(request, id):
    subject= Subject.objects.get(subjectid=id)

    if request.session.has_key('username') and subject.isenable == 1:
        account = Account.objects.get(username=request.session['username'])
        if request.session.has_key('look'):
            lookbf = request.session['look']
        else:
            lookbf = '0'
        
        if boolcheckEnroll(subject, request.session['username']):
            subject = Subject.objects.get(subjectid = id)
            username = request.session['username']
            arrChapLes = getChapterLessson(subject, account)
            chapterShow = Chapter.objects.get(chapterid = getNumInString(arrChapLes[0].chapterid))
            listchapter = getProcessChapter(subject, account)
            chapcomplete = listchapter[len(listchapter)-1].iscomplete
           
            context={
                'account':account,
                'subject':subject,
                'username':username,
                'arrChapLes':arrChapLes,
                'chapterShow':chapterShow,
                'listchapter':listchapter,
                'chapcomplete':chapcomplete,

                'lookbf': lookbf
            }
            return render(request, 'course/coursechapter.html',context)
        else:
            return redirect('course:coursedetail', id=subject.subjectid)
        
    else:
        return redirect('course:coursedetail', id=subject.subjectid)

def courselesson(request, idsub, idchap, idles):
    subject= Subject.objects.get(subjectid=idsub)
    chapter = Chapter.objects.get(chapterid=idchap)
    lesson = Lesson.objects.get(lessonid = idles)
    
    if request.session.has_key('username') and subject.isenable ==1 :
        account = Account.objects.get(username=request.session['username'])
        if boolcheckEnroll(subject, request.session['username']):
            subject = Subject.objects.get(subjectid = idsub)
            username = request.session['username']
            arrItemAct = getItemActivity(lesson)
            
            # reply lesson
            lessonreplies = LessonReply.objects.filter(lessonid = idles).order_by('-createdate')
            num = len(lessonreplies)
            if num > 2:
                showlessonreps = lessonreplies[0:2]
            else:
                showlessonreps = lessonreplies
            LesandAcc = []
            for showlessonrep in showlessonreps:
                enrollment = showlessonrep.enrollmentid
                acc = enrollment.accountid
                showlessonrep.lessonreplyid = 'check(' + str(showlessonrep.lessonreplyid) + ')'
                temp = LessonReplyAccount(showlessonrep, acc)
                LesandAcc.append(temp)

            # Comment
            if request.method == 'POST':
                decrip = request.POST.get('description')
                lessonRep = LessonReply(
                    content = decrip,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    isenable = 1,
                    note = '',
                    lessonid = lesson,
                    enrollmentid = Enrollment.objects.filter(accountid=account).get(subjectid =subject)
                )
                lessonRep.save()
                
                return redirect('course:courselesson', idsub=subject.subjectid, idchap=chapter.chapterid, idles=lesson.lessonid)

            context={
                'account':account,
                'subject':subject,
                'username':username,
                'chapter':chapter,
                'lesson':lesson,
                'arrItemAct':arrItemAct,
                'LesandAcc':LesandAcc,
            }
            return render(request, 'course/courselesson.html', context)
        else:
            return redirect('course:coursedetail', id=subject.subjectid)
        
    else:
        return redirect('course:coursedetail', id=subject.subjectid)
    
def courseactivity(request, idsub, idchap, idles, iditem, idact):
    subject= Subject.objects.get(subjectid=idsub)
    chapter = Chapter.objects.get(chapterid=idchap)
    lesson = Lesson.objects.get(lessonid = idles)
    item = Item.objects.get(itemid = iditem)
    activity = Activity.objects.get(activityid = idact)

    if request.session.has_key('username') and subject.isenable==1:
        account = Account.objects.get(username=request.session['username'])
        if request.session.has_key('look'):
            sesslook = request.session['look']
        else:
            sesslook = 0
        if boolcheckEnroll(subject, request.session['username']) and boolcheckUnlockChapter(chapter, account, sesslook):
            subject = Subject.objects.get(subjectid = idsub)
            username = request.session['username']
            arrItemAct = getItemActivity(lesson)
            # activity reply
            actReplies = ActivityReply.objects.filter(activityid=activity).order_by('-createdate')
            num = len(actReplies)
            if num > 2:
                showactreplies = actReplies[0:2]
            else:
                showactreplies = actReplies
            ActandAcc = []
            for showactreply in showactreplies:
                enrollment = showactreply.enrollmentid
                acc = enrollment.accountid
                showactreply.activityreplyid = 'check(' + str(showactreply.activityreplyid) + ')'
                temp = ActivityReplyAccount(showactreply, acc)
                ActandAcc.append(temp)
            listactivity=getProcessActivity(activity,account)
            lescomplete=listactivity[len(listactivity)-1].iscomplete
            #chuyen ten hoat dong thanh hd + order
            for act in listactivity:
                act.activity.activityname= "Hoạt Động " +str(act.order)
            # Kiem tra hoat dong tien quyet
            try:
                requireact = activity.requiredactivityid
            except:
                requireact = None
           
            if requireact != None:
                checkreact = boolcheckActivityTracking(requireact,account)
                if sesslook != 0:
                    checkreact = 1
            else:
                checkreact = 1
            
            if checkreact == 0:
                requitem = requireact.itemid
                context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'requireact':requireact,
                    'requitem':requitem,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete
                }
                # Chọn HD
                if activity.activitytypeid.activitytypeid == 1:
                    return render(request, 'course/courseactivityEBOOK.html', context)
                elif activity.activitytypeid.activitytypeid == 2:
                    return render(request, 'course/courseactivityPDF.html', context)
                elif activity.activitytypeid.activitytypeid == 3:
                    return render(request, 'course/courseactivityVIDEO.html', context)
                elif activity.activitytypeid.activitytypeid == 4:
                    return render(request, 'course/courseactivitySCORM.html', context)
                elif activity.activitytypeid.activitytypeid == 5:
                    return render(request, 'course/courseactivityGAME.html', context)
                elif activity.activitytypeid.activitytypeid == 6:
                    return render(request, 'course/courseactivitySUBMIT.html', context)
                elif activity.activitytypeid.activitytypeid == 7:
                    return render(request, 'course/courseactivityMULMEDIA.html', context)
            
            elif checkreact == 1:
                
                # Chọn HD
                if activity.activitytypeid.activitytypeid == 1:
                    context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete
                    }
                    return render(request, 'course/courseactivityEBOOK.html', context)
                elif activity.activitytypeid.activitytypeid == 2:
                    namePDF = getNamePDF(activity.link)
                    context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'namePDF':namePDF,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete
                    }
                    return render(request, 'course/courseactivityPDF.html', context)
                elif activity.activitytypeid.activitytypeid == 3:
                    context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete
                    }
                    return render(request, 'course/courseactivityVIDEO.html', context)
                elif activity.activitytypeid.activitytypeid == 4:
                    context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete
                    }
                    return render(request, 'course/courseactivitySCORM.html', context)
                
                elif activity.activitytypeid.activitytypeid == 5:
                    context = {
                        'account':account,
                        'subject':subject,
                        'username':username,
                        'chapter':chapter,
                        'lesson':lesson,
                        'item':item,
                        'activity':activity,
                        'arrItemAct':arrItemAct,
                        'ActandAcc':ActandAcc,
                        'checkreact':checkreact,
                        'listactivity':listactivity,
                        'lescomplete':lescomplete
                    }
                    return render(request, 'course/courseactivityGAME.html', context)
                elif activity.activitytypeid.activitytypeid == 6:
                    # Lấy HD
                    actsub = ActivitySubmittion.objects.filter(activityid=activity.activityid).filter(accountid=account.accountid)
                    if len(actsub) != 0:
                        issub=1
                        arrAS = []
                        for actsubt in actsub:
                            actsubt.link = actsubt.link.replace('/media/','')
                            arrAS.append(actsubt)
                    else:
                        issub=0
                    # POST SUBMIT 
                    if request.method == "POST":
                        try:
                            fileSM =  request.FILES.get("fileSM")
                        except:
                            fileSM = None
                        descripSM = request.POST.get("descripSM")
                        
                        if fileSM != None:
                            fileURL = tokenFile(fileSM)
                        else:
                            fileURL = ''
                        contentf= request.POST.get("sizeoffile")
                        actSubMit = ActivitySubmittion(
                            accountid = account,
                            activityid = activity,
                            createdate = datetime.now(),
                            editdate = datetime.now(),
                            link = fileURL,
                            description = descripSM,
                            content = contentf,
                            isenable = 1,
                            note = '',
                        )
                        actSubMit.save()

                        # Tracking activity
                        enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject)
                        try:
                            tracking = Tracking.objects.filter(enrollmentid = enrollment).get(activityid = activity)
                            tracking.isenable = 1
                            tracking.save()
                        except:
                            # lấy subpart
                            subpart = SubjectPart.objects.filter(subjectid = subject).get(order = 1)

                            track = Tracking(
                                createdate  = datetime.now(),
                                editdate = datetime.now(),
                                isenable = 1,
                                note = '',
                                activityid = activity,
                                itemid = item,
                                lessonid = lesson,
                                enrollmentid = enrollment,
                                subjectid = subject,
                                chapterid = chapter,
                                subjectpartid = subpart,
                            )

                            track.save()

                        return redirect('course:courseactivity', idsub=subject.subjectid, idchap=chapter.chapterid, idles=lesson.lessonid, iditem=item.itemid, idact=activity.activityid)

                    
                    if issub == 1:
                        context = {
                            'account':account,
                            'subject':subject,
                            'username':username,
                            'chapter':chapter,
                            'lesson':lesson,
                            'item':item,
                            'activity':activity,
                            'arrItemAct':arrItemAct,
                            'ActandAcc':ActandAcc,
                            'checkreact':checkreact,
                            'listactivity':listactivity,
                            'lescomplete':lescomplete,
                            'actsub':arrAS[len(arrAS)-1],
                            'issub':issub,
                            'numSM':len(arrAS)
                        }
                    else:
                        context = {
                            'account':account,
                            'subject':subject,
                            'username':username,
                            'chapter':chapter,
                            'lesson':lesson,
                            'item':item,
                            'activity':activity,
                            'arrItemAct':arrItemAct,
                            'ActandAcc':ActandAcc,
                            'checkreact':checkreact,
                            'listactivity':listactivity,
                            'lescomplete':lescomplete,
                           
                            'issub':issub,
                        }   

                    return render(request, 'course/courseactivitySUBMIT.html', context)
                elif activity.activitytypeid.activitytypeid == 7:
                    linkall=activity.link.split(" ")
                    linksc=linkall[0]
                    linkpd=getNamePDF(linkall[1])
                    linkvid=linkall[2]
                    context={
                    'account':account,
                    'subject':subject,
                    'username':username,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'activity':activity,
                    'arrItemAct':arrItemAct,
                    'ActandAcc':ActandAcc,
                    'checkreact':checkreact,
                    'listactivity':listactivity,
                    'lescomplete':lescomplete,
                    'linksc':linksc,
                    'linkpd':linkpd,
                    'linkvid':linkvid,
                    }
                    return render(request, 'course/courseactivityMULMEDIA.html', context)
        else:
            return redirect('course:coursedetail', id=subject.subjectid)     
    else:
        return redirect('course:coursedetail', id=subject.subjectid)
    
def pdfView(request, namePDF):
    link = './media/' + namePDF + ".pdf"
    pdf_data = open(link, "rb").read()
    return HttpResponse(pdf_data, content_type='application/pdf')

# Các khóa học của người học đã đang kí
def courselist(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        # Lấy enroll của account
        enrollments = Enrollment.objects.filter(accountid = account)
        listsubject = []
        for enrollment in enrollments:
            listsubject.append(enrollment.subjectid)
        arrRate = []
        for i in range(len(listsubject)):
            arrRate.append(getrateSubject(listsubject[i]))
        arrSubMas = []
        for i in range(len(listsubject)):
            subcate = listsubject[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(listsubject[i],arrRate[i][0],arrRate[i][1],converttimetoString(arrRate[i][2]),getlikeSubjectId(listsubject[i]),enviromentcate.enviromentcatename)
            arrSubMas.append(temp)

        context = {
            'account':account,
            'arrSubMas':arrSubMas
        }
        return render(request, 'course/courseList.html', context)
    else:
        return redirect('homepage:index')
    
def teacherdetail(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        context = {
            'account':account
        }
        return render(request, 'course/teacherdetail.html',context)
    else:
        return redirect('homepage:index')

def teachercourse(request, teacheraccid):
    show = 1
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        subjects1QR = Subject.objects.filter(accountid=teacheraccid).filter(isenable=1)
        subjects1 = []
        for subject1QR in subjects1QR:
            subjects1.append(subject1QR)
        subjectteachers2 = SubjectTeacher.objects.filter(accountid = teacheraccid)
        subjects2 = []
        for subjectteacher2 in subjectteachers2:
            if subjectteacher2.subjectid.isenable == 1:
                subjects2.append(subjectteacher2.subjectid)
        subjects = subjects1 + subjects2
        if len(subjects) == 0:
            show = 0
            context = {
                'show':show,
                'islog':islog,
                'account':account
            }
            return render(request, 'course/courseteacherList.html',context)
        # Xu ly
        # Lấy mảng rate
        arrTup = []
        for i in range(len(subjects)):
            arrTup.append(getrateSubject(subjects[i]))
        # Tạo mảng có biến class SubjectMaster
        arrSubMas = []
        for i in range(len(subjects)):
            # Lấy cate
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrTup[i][0],arrTup[i][1],converttimetoString(arrTup[i][2]),getlikeSubjectId(subjects[i]), enviromentcate.enviromentcatename)
            arrSubMas.append(temp)
        context = {
            'arrSubMas':arrSubMas,
            'show':show,
            'islog':islog,
            'account':account
        }
        return render(request, 'course/courseteacherList.html', context)
    else:
        islog = 0
        subjects1QR = Subject.objects.filter(accountid=teacheraccid).filter(isenable=1)
        subjects1 = []
        for subject1QR in subjects1QR:
            subjects1.append(subject1QR)
        subjectteachers2 = SubjectTeacher.objects.filter(accountid = teacheraccid)
        subjects2 = []
        for subjectteacher2 in subjectteachers2:
            if subjectteacher2.subjectid.isenable == 1:
                subjects2.append(subjectteacher2.subjectid)
        subjects = subjects1 + subjects2
        if len(subjects) == 0:
            show = 0
            context = {
                'show':show,
                'islog':islog
            }
            return render(request, 'course/courseteacherList.html',context)
        # Xu ly
        # Lấy mảng rate
        arrTup = []
        for i in range(len(subjects)):
            arrTup.append(getrateSubject(subjects[i]))
        # Tạo mảng có biến class SubjectMaster
        arrSubMas = []
        for i in range(len(subjects)):
            # Lấy cate
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrTup[i][0],arrTup[i][1],converttimetoString(arrTup[i][2]),getlikeSubjectId(subjects[i]), enviromentcate.enviromentcatename)
            arrSubMas.append(temp)
        context = {
            'arrSubMas':arrSubMas,
            'show':show,
            'islog':islog
        }
        return render(request, 'course/courseteacherList.html', context)

def managecourse(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2:
            # xu ly
            subjects1QR = Subject.objects.filter(accountid=account).exclude(isenable=3).order_by('-createdate')
            subjects1 = []
            for subject1QR in subjects1QR:
                subjects1.append(subject1QR)
            subjectteachers2 = SubjectTeacher.objects.filter(accountid = account)
            subjects2 = []
            for subjectteacher2 in subjectteachers2:
                subjects2.append(subjectteacher2.subjectid)
            subjects = subjects1 + subjects2
            
            environments = EnviromentCate.objects.all()
            if len(subjects) == 0:
                context = {
                    'account':account,
                    'environments':environments,
                }
                return render(request, 'course/managecourse.html', context)
            # Lấy mảng rate
            arrTup = []
            for i in range(len(subjects)):
                arrTup.append(getrateSubject(subjects[i]))


            
            # Tạo mảng có biến class SubjectMaster
            arrSubMas = []
            for i in range(len(subjects)):
                # Lấy cate
                subcate = subjects[i].enviromentcateid
                enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
                temp = SubjectMaster(subjects[i],arrTup[i][0],arrTup[i][1],converttimetoString(arrTup[i][2]),getlikeSubjectId(subjects[i]), enviromentcate.enviromentcatename)
                arrSubMas.append(temp)
            
            context = {
                'account':account,
                'arrSubMas':arrSubMas,
                'environments': environments,
            }
            return render(request, 'course/managecourse.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def managesubmition(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2:
            # xu ly
            subjects1QR = Subject.objects.filter(accountid=account).exclude(isenable=3).order_by('-createdate')
            subjects1 = []
            for subject1QR in subjects1QR:
                subjects1.append(subject1QR)
            subjectteachers2 = SubjectTeacher.objects.filter(accountid = account)
            subjects2 = []
            for subjectteacher2 in subjectteachers2:
                subjects2.append(subjectteacher2.subjectid)
            subjects = subjects1 + subjects2


            
            context = {
                'account':account,
                'subjects': subjects,
            }
            return render(request, 'course/managesubmition.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
    return render(request, 'course/managesubmition.html')

def reviewsubmition(request,idsubmit):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        activitysubmittion =ActivitySubmittion.objects.get(activitysubmittionid=idsubmit)
        activity =activitysubmittion.activityid
        item=activity.itemid
        lesson=item.lessonid
        chapter=lesson.chapterid
        subject=chapter.subjectid

        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account,subject):
        
            context = {
                'account':account,
                'activitysubmittion':activitysubmittion
            }
            return render(request, 'course/reviewsubmit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
    
   
    
def managecourseteacher(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2:
            subjects = Subject.objects.filter(accountid=account).exclude(isenable=3).order_by('-createdate')
            environments = EnviromentCate.objects.all()
            
            searsubs = []
            for subject in subjects:
                searsubs.append(subject.subjectname)
            
            accounts = Account.objects.exclude(accounttypeid=3).exclude(accountid=account.accountid)
            tea = []
            for acc in accounts:
                userdetail = UserDetail.objects.get(accountid = acc)
                temp = AccountUserdetail(acc, userdetail)
                tea.append(temp)
            teachers = []
            for t in tea:
                teachers.append(t.userdetail.lastname + ' ' + t.userdetail.firstname + ' - ' + t.account.username)

            


            context = {
                'teachers':teachers,
                'account':account,
                'searsubs':searsubs,
                'subjects': subjects,
                'environments': environments,
            }
            return render(request, 'course/manageteach.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
# COURSE

def coursecreate(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2):
            enviromentcates = EnviromentCate.objects.all()

            if request.method == "POST":
                enrollcateid = request.POST.get('enviromentcateid')
                subname = request.POST.get('subjectname')
                descrip = request.POST.get('description')
                cont = request.POST.get('content')
                infoVD = request.POST.get('video')
                
                try:
                    imgSub = request.FILES.get('avatar')
                except:
                    imgSub = None
                
                note = request.POST.get('note')

                if imgSub != None:
                    imgSubURL = tokenFile(imgSub)
                else:
                    imgSubURL = ''

                chapterNum = request.POST.get('chapterNum')


                subjectNew = Subject(
                    enviromentcateid = EnviromentCate.objects.get(enviromentcateid=enrollcateid),
                    subjectname = subname,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    description = descrip,
                    isenable = 0,
                    note = note,
                    accountid = account,
                    introvideo = getEmbedYoutube(infoVD),
                    content = cont,
                    avatar = imgSubURL,
                )
                subjectNew.save()
                # Khoi tao 4 subjectpart ban dau 
                subpartnew1= SubjectPart(
                    isenable=1,
                    note="",
                    accountid=account,
                    subjectid=subjectNew,
                    createdate=datetime.now(),
                    description="",
                    editdate = datetime.now(),
                    subjectpartname  = "Nào ta cùng học",
                    content = '',
                    avatar = '/media/bc_baihoc.png',
                    order = 1
                )
                subpartnew1.save()

                subpartnew2= SubjectPart(
                    isenable=1,
                    note="",
                    accountid=account,
                    subjectid=subjectNew,
                    createdate=datetime.now(),
                    description="",
                    editdate = datetime.now(),
                    subjectpartname  = "Thế giới trò chơi",
                    content = '',
                    avatar = '/media/bc_trochoi.png',
                    order = 2
                )
                subpartnew2.save()

                subpartnew3= SubjectPart(
                    isenable=1,
                    note="",
                    accountid=account,
                    subjectid=subjectNew,
                    createdate=datetime.now(),
                    description="",
                    editdate = datetime.now(),
                    subjectpartname  = "Dự Án Của Em",
                    content = '',
                    avatar = '/media/bc_chiaseduan.png',
                    order = 3
                )
                subpartnew3.save()

                subpartnew4= SubjectPart(
                    isenable=1,
                    note="",
                    accountid=account,
                    subjectid=subjectNew,
                    createdate=datetime.now(),
                    description="",
                    editdate = datetime.now(),
                    subjectpartname  = "Cùng Nhau Thảo Luận",
                    content = '',
                    avatar = '/media/bc_diendang.png',
                    order = 4
                )
                subpartnew4.save()

                chapterNum = int(chapterNum)
                if chapterNum > 0:
                    for i in range(1,chapterNum+1):
                        # Khởi tạo Chương
                        chapterNew = Chapter(
                            accountid = account,
                            subjectid = subjectNew,
                            chaptername = request.POST.get(str(i)),
                            createdate = datetime.now(),
                            editdate = datetime.now(),
                            isenable = 1,
                            description = '',
                            content = '',
                            order = i,
                            note = '',
                        )
                        chapterNew.save()


                return redirect('course:managecourse')

            context={
                'account':account,
                'enviromentcates': enviromentcates
            }
            return render(request, 'course/coursecreate.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def courseedit(request, idsub):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        enviromentcates = EnviromentCate.objects.all()
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            subject.avatar=subject.avatar.replace('/media/','')
            if request.method == 'POST':
                enrollcateid = request.POST.get('enviromentcateid')
                subname = request.POST.get('subjectname')
                descrip = request.POST.get('description')
                cont = request.POST.get('content')
                
                infoVD = request.POST.get('video')
                if infoVD=='':
                    infoVD = subject.introvideo
               
                try:
                    imgSub = request.FILES.get('avatar')
                except:
                    imgSub = None
              
                note = request.POST.get('note')
                
                if imgSub != None:
                    imgSubURL = tokenFile(imgSub)
                else:
                    imgSubURL = '/media/'+subject.avatar
                
           
                subject.enviromentcateid = EnviromentCate.objects.get(enviromentcateid=enrollcateid)
                subject.subjectname = subname
                subject.editdate = datetime.now()
                subject.description = descrip
                subject.note = note
                subject.introvideo = getEmbedYoutube(infoVD)
                subject.content = cont
                subject.avatar = imgSubURL
                subject.save()

                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'enviromentcates':enviromentcates,
                'subject':subject,
                'account':account,
            }
            return render(request,"course/courseedit.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')



# CHAP
def chapincourse(request, idsub):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            
            chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
            i = 1
            for chap in chapters:
                chap.chaptername = 'Bài ' + str(i) + ': ' + chap.chaptername
                i += 1
            # POST SUBMIT PUBLIC or NOT SUBJECT
            if request.method == "POST":
                userdetail = UserDetail.objects.get(accountid = account)
                if subject.isenable == 0:
                    
                    # subject.isenable = 1
                    s1 = 'Công khai khóa học: ' + subject.subjectname
                    s2 = 'NAME: ' + subject.subjectname + '(' + str(subject.subjectid) + ') FROM ( USERNAME: ' + account.username + ') --- EMAIL: ' + userdetail.email
                    send_mail(s1,
                        s2,
                        'vsprodhsp@gmail.com',
                        ['vsprosuperuser@gmail.com'],
                        fail_silently=False
                    )
                elif subject.isenable == 1:
                    s1 = 'Ngưng công khai khóa học: ' + subject.subjectname
                    s2 = 'NAME: ' + subject.subjectname + '(' + str(subject.subjectid) + ') FROM ( USERNAME: ' + account.username + ') --- EMAIL: ' + userdetail.email
        
                    send_mail(s1,
                        s2,
                        'vsprodhsp@gmail.com',
                        ['vsprosuperuser@gmail.com'],
                        fail_silently=False
                    )
                    subject.isenable = 0

                subject.save()

                return redirect('course:managecourse')

            context={
                'subject':subject,
                'account':account,
                'chapters':chapters,
            }
            return render(request,"course/chapincourse.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
    
def chaptercreate(request, idsub):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == 'POST':
                chaptername = request.POST.get('chaptername')
                description = request.POST.get('description')
                content = request.POST.get('content')
                
                note = request.POST.get('note')
                

                chapterNew = Chapter(
                    accountid = account,
                    subjectid = subject,
                    chaptername = chaptername,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    isenable = 1,
                    description = description,
                    content = content,
                    note = note,
                    order = len(Chapter.objects.filter(subjectid = subject)) + 1
                )
                chapterNew.save()
                
                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'subject':subject,
                'account':account,
            }
            return render(request,"course/chaptercreate.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def chapteredit(request, idsub, idchap):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
      
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            chapter = Chapter.objects.get(chapterid=idchap)
            
            if request.method == 'POST':
                chaptername = request.POST.get('chaptername')
                description = request.POST.get('description')
                content = request.POST.get('content')
                note = request.POST.get('note')
                

                chapter.chaptername = chaptername
                chapter.editdate = datetime.now()
                chapter.description = description
                chapter.content = content
                chapter.note = note
            
                chapter.save()

                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'chapter':chapter,
                'subject':subject,
                'account':account,
            }
            return render(request,"course/chapteredit.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

# LESSON

def lessinchap(request, idsub, idchap):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid=idchap)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            
            lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
            i = 1
            for les in lessons:
                les.lessonname = 'Chủ đề ' + str(i) + ': ' + les.lessonname
                i += 1
            context={
                'subject':subject,
                'account':account,
                'lessons':lessons,
                'chapter':chapter,
            }
            return render(request,"course/lessinchap.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def lessoncreate(request, idsub, idchap):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid = idchap)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == 'POST':
                lesname = request.POST.get('lesname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                note = request.POST.get('note')

                lessonNew = Lesson(
                    accountid = account,
                    chapterid = chapter,
                    lessonname = lesname,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    isenable = 1,
                    description = description,
                    content = content,
                    note = note,
                    order = len(Lesson.objects.filter(chapterid = chapter)) + 1
                )
                lessonNew.save()
                
                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'chapter':chapter,
                'account':account,
            }
            return render(request,"course/lessoncreate.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def lessonedit(request, idsub, idchap, idles):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
      
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            chapter = Chapter.objects.get(chapterid=idchap)
            lesson = Lesson.objects.get(lessonid = idles)
            if request.method == 'POST':
                lesname = request.POST.get('lesname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                note = request.POST.get('note')
                

                lesson.lessonname = lesname
                lesson.editdate = datetime.now()
                lesson.description = description
                lesson.content = content
                lesson.note = note
            
                lesson.save()
                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'lesson':lesson,
                'chapter':chapter,
                'subject':subject,
                'account':account,
            }
            return render(request,"course/lessonedit.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

# ITEM

def iteminles(request, idsub, idchap, idles):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid=idchap)
        lesson = Lesson.objects.get(lessonid = idles)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            
            items = Item.objects.filter(lessonid = lesson).order_by('order')
            i = 1
            for item in items:
                item.itemname = str(i) + '/ ' + item.itemname
                i += 1
            
            context={
                'items':items,
                'subject':subject,
                'account':account,
                'lesson':lesson,
                'chapter':chapter,
            }
            return render(request,"course/iteminles.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def itemcreate(request, idsub, idchap, idles):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid = idchap)
        lesson= Lesson.objects.get(lessonid = idles)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == 'POST':
                itemname = request.POST.get('itemname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                note = request.POST.get('note')

                itemNew = Item(
                    accountid = account,
                    lessonid = lesson,
                    itemname = itemname,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    isenable = 1,
                    description = description,
                    content = content,
                    note = note,
                    order = len(Item.objects.filter(lessonid = lesson)) + 1
                )
                itemNew.save()
                
                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'lesson': lesson,
                'chapter':chapter,
                'account':account,
            }
            return render(request,"course/itemcreate.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def itemedit(request, idsub, idchap, idles,iditem):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)

        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            chapter = Chapter.objects.get(chapterid=idchap)
            lesson = Lesson.objects.get(lessonid = idles)
            item = Item.objects.get(itemid=iditem)
            if request.method == 'POST':
                itemname = request.POST.get('itemname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                note = request.POST.get('note')

                item.itemname = itemname
                item.editdate = datetime.now()
                item.description = description
                item.content = content
                item.note = note
               
                item.save()
                
                return redirect('course:courseoverview', idsub=subject.subjectid)

            context={
                'item':item,
                'chapter':chapter,
                'account':account,
                'lesson':lesson,
            }
            return render(request,"course/itemedit.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

# ACT

def actinitem(request, idsub, idchap, idles, iditem):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid=idchap)
        lesson = Lesson.objects.get(lessonid = idles)
        item = Item.objects.get(itemid = iditem)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            
            activities = Activity.objects.filter(itemid = item).order_by('order')
            i = 1
            for activity in activities:
                activity.activityname = 'Hoạt động ' + str(i) + ': ' + activity.activityname
                i += 1
            
            context={
                'activities':activities,
                'item':item,
                'subject':subject,
                'account':account,
                'lesson':lesson,
                'chapter':chapter,
            }
            return render(request,"course/actinitem.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def activitycreate(request, idsub, idchap, idles, iditem):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid = idchap)
        lesson= Lesson.objects.get(lessonid = idles)
        item = Item.objects.get(itemid = iditem)
        activitytypes = ActivityType.objects.all()
        items = Item.objects.filter(lessonid=lesson)
        arract =[]
        for ite in items:
            acts = Activity.objects.filter(itemid = ite)
            for act in acts:
                arract.append(act)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == "POST":
                acttype = request.POST.get('activitytypeid')   
                

                requireact = request.POST.get('requireact')
                actname = request.POST.get('actname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                time = request.POST.get('time')
               
                if acttype == '3':
                    linkyoutube = request.POST.get('linkyoutube')
                    linkyoutube = getEmbedYoutube(linkyoutube)
                    nameScorm = linkyoutube
                else:
                    try:
                        avatar = request.FILES.get('avatar')
                    except:
                        avatar = None
                    if avatar!=None:
                        urlavatar = tokenFile(avatar)
                    else:
                        urlavatar = ''
                    nameScorm = urlavatar
                
                if requireact == 'NULL':
                    requireact = None
                else:
                    requireact = Activity.objects.get(activityid = requireact)
                        

                    
                note = request.POST.get('note')
                # html m dislay none t bỏ require rồi, nếu !3 thì ko lấy file lu
               
                
                if acttype == '4' or acttype == '5':
                    if urlavatar != '':
                      
                        nameScorm = nameScorm.replace('/media/','')
                        nameScorm = nameScorm.replace('.zip','')
                        s = '.' + urlavatar   
                    #    s = '.'
                    #    m = "'\\'"
                    #    for i in urlavatar:
                    #        if i == '/':
                    #            s += m
                    #        else:
                    #            s += i

                    unzip = ZipFile(s)
                    urlunzip='./media/unzip/' + nameScorm
                    unzip.extractall(urlunzip)
                    unzip.close
                    nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                
                actNew = Activity(
                    accountid =  account,                 
                    requiredactivityid = requireact,
                    itemid = item,
                    activitytypeid = ActivityType.objects.get(activitytypeid = acttype),
                    activityname = actname,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    time =time,
                    isenable = 1,
                    description=description,
                    content=content,
                    link=nameScorm,
                    order= len(Activity.objects.filter(itemid=item))+1,
                    note=note,
                )

                actNew.save()

                

                return redirect('course:courseoverview', idsub=subject.subjectid)


            context={
                'activitytypes':activitytypes,
                'arract':arract,
                'subject':subject,
                'chapter':chapter,
                'lesson':lesson,
                'item':item,
                'account':account,
            }
            return render(request,"course/activitycreate.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

## special act
def activitySPECcreate(request, idsub, idchap, idles, iditem):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid = idchap)
        lesson= Lesson.objects.get(lessonid = idles)
        item = Item.objects.get(itemid = iditem)
        activitytypes = ActivityType.objects.all()
        items = Item.objects.filter(lessonid=lesson)
        arract =[]
        for ite in items:
            acts = Activity.objects.filter(itemid = ite)
            for act in acts:
                arract.append(act)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == "POST":
                # acttype = request.POST.get('activitytypeid')   
                

                requireact = request.POST.get('requireact')
                actname = request.POST.get('actname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                time = request.POST.get('time')
                try:
                    avatar = request.FILES.get('scorm')
                except:
                    avatar = None
                note = request.POST.get('note')

                if avatar!=None:
                    urlavatar = tokenFile(avatar)
                else:
                    urlavatar = ''
                if requireact == 'NULL':
                    requireact = None
                else:
                    requireact = Activity.objects.get(activityid = requireact)

                nameScorm = urlavatar
                if urlavatar != '':
                      
                    nameScorm = nameScorm.replace('/media/','')
                    nameScorm = nameScorm.replace('.zip','')
                    s = '.' + urlavatar   
                    # s = '.'
                    # m = "\\"
                    # for i in urlavatar:
                    #     if i == '/':
                    #         s += m
                    #     else:
                    #         s += i

                unzip = ZipFile(s)
                urlunzip='./media/unzip/' + nameScorm
                unzip.extractall(urlunzip)
                unzip.close
                nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                
                # pdf
                try:
                    pdf = request.FILES.get('pdf')
                except:
                    pdf = None
                
                if pdf != None:
                    linkpdf = tokenFile(pdf)
                else:
                    linkpdf = ''
                # video
                video = request.POST.get('videoyoutube')
              
                if video != '':
                    linkvideo = getEmbedYoutube(video)
                else:
                    linkvideo = ''
                
                # Link cộng
                link = nameScorm + ' ' + linkpdf + ' ' + linkvideo



                actNew = Activity(
                    accountid =  account,                 
                    requiredactivityid = requireact,
                    itemid = item,
                    activitytypeid = ActivityType.objects.get(activitytypeid = 7),
                    activityname = actname,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    time =time,
                    isenable = 1,
                    description=description,
                    content=content,
                    link=link,
                    order= len(Activity.objects.filter(itemid=item))+1,
                    note=note,
                )

                actNew.save()

                

                return redirect('course:courseoverview', idsub=subject.subjectid)


            context={
                'activitytypes':activitytypes,
                'arract':arract,
                'subject':subject,
                'chapter':chapter,
                'lesson':lesson,
                'item':item,
                'account':account,
            }
            return render(request,"course/activitycreate2.html",context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')







def activityedit(request, idsub, idchap, idles, iditem,idact):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        chapter = Chapter.objects.get(chapterid = idchap)
        lesson= Lesson.objects.get(lessonid = idles)
        item = Item.objects.get(itemid = iditem)
        activitytypes = ActivityType.objects.all()
        items = Item.objects.filter(lessonid=lesson)
        activity = Activity.objects.get(activityid= idact)
        
        # HD 7:
        if activity.activitytypeid.activitytypeid == 7:
            link = activity.link.split(' ')
            linkscm = link[0].replace('/media/unzip/',"")
            linkpdf = link[1].replace('/media/',"")
            linkvid = link[2].replace("/media/", "")
        else:
            try:
                if activity.activitytypeid.activitytypeid == 4 or activity.activitytypeid.activitytypeid == 5:
                    linkact = activity.link.replace("/media/unzip/", "")
                else:
                    linkact = activity.link.replace("/media/", "")
            except:
                linkact = 1
            if linkact == '':
                linkact = 1
        
        arract =[]
        for ite in items:
            acts = Activity.objects.filter(itemid = ite)
            for act in acts:
                arract.append(act)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject):
            if request.method == "POST":
                if activity.activitytypeid.activitytypeid != 7 and activity.activitytypeid.activitytypeid != 3 :
                    acttype = request.POST.get('activitytypeid')
                else:
                    if activity.activitytypeid.activitytypeid == 7:
                        acttype = 7
                    else:
                        acttype = 3
                requireact = request.POST.get('requireact')
                actname = request.POST.get('actname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                time = request.POST.get('time')
                note = request.POST.get('note')
                if requireact == 'NULL':
                    requireact = None
                
                try:
                    avatar = request.FILES.get('avatar')
                except:
                    avatar = None
                
                
               
               # HD tu 1 -> 6
                if acttype != 7:
                    if acttype == 3:
                        linkyoutube = request.POST.get('linkyoutube')
                        if linkyoutube != '':
                            linkyoutube = getEmbedYoutube(linkyoutube)
                            nameScorm = linkyoutube
                        else:
                            nameScorm = activity.link
                    else:
                        if avatar != None:
                            urlavatar = tokenFile(avatar)
                        else:
                            urlavatar = activity.link
                        
                        nameScorm = urlavatar
                        
                        if acttype == '4' or acttype == '5':
                            if urlavatar !=  activity.link :
                            
                                nameScorm = nameScorm.replace('/media/','')
                                nameScorm = nameScorm.replace('.zip','')
                                s = '.' + urlavatar   
                                # s = '.'
                                # m = "\\"
                                # for i in urlavatar:
                                #     if i == '/':
                                #         s += m
                                #     else:
                                #         s += i

                                unzip = ZipFile(s)
                                urlunzip='./media/unzip/' + nameScorm
                                unzip.extractall(urlunzip)
                                unzip.close
                                nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                # HD 7
                else:
                    if avatar != None:
                        urlavatar = tokenFile(avatar)
                    else:
                        urlavatar = link[0]
                    
                    nameScorm = urlavatar
                    if urlavatar !=  link[0]:
                        
                        nameScorm = nameScorm.replace('/media/','')
                        nameScorm = nameScorm.replace('.zip','')
                        s = '.' + urlavatar   
                        # s = '.'
                        # m = "\\"
                        # for i in urlavatar:
                        #     if i == '/':
                        #         s += m
                        #     else:
                        #         s += i

                        unzip = ZipFile(s)
                        urlunzip='./media/unzip/' + nameScorm
                        unzip.extractall(urlunzip)
                        unzip.close
                        nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                    
                    try:
                        pdf = request.FILES.get('pdf')
                    except:
                        pdf = None
                        
                    if pdf != None:
                        linkpdf = tokenFile(pdf)
                    else:
                        linkpdf = link[1]
                    # video
                    try:
                        video = request.FILES.get('video')
                    except:
                        video = None
                        
                    if video != None:
                        linkvideo = tokenFile(video)
                    else:
                        linkvideo = link[2]
                    
                    # Link cộng
                    nameScorm = nameScorm + ' ' + linkpdf + ' ' + linkvideo
                



                if requireact != None:              
                    activity.requiredactivityid = Activity.objects.get(activityid=requireact) 
                else:
                    activity.requiredactivityid = None
                activity.activitytypeid = ActivityType.objects.get(activitytypeid = acttype)
                activity.activityname = actname
                activity.editdate = datetime.now()
                activity.time =time
                activity.description=description
                activity.content=content
                if nameScorm != '':
                    activity.link=nameScorm
                
                activity.note=note

                activity.save()

                return redirect('course:courseoverview', idsub=subject.subjectid)
        
            if activity.activitytypeid.activitytypeid == 7:
                context={
                   'linkscm':linkscm,
                    'linkpdf':linkpdf, 
                    'linkvid':linkvid,
                    'activity':activity,
                    'activitytypes':activitytypes,
                    'arract':arract,
                    'subject':subject,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'account':account,
                }
            else:
                context={
                    'linkact': linkact,
                    'activity':activity,
                    'activitytypes':activitytypes,
                    'arract':arract,
                    'subject':subject,
                    'chapter':chapter,
                    'lesson':lesson,
                    'item':item,
                    'account':account,
                }
            return render(request,'course/activityedit.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
 
def showsubjectsbyenvironment(request, idcate):
    #  KT dang nhap
    env = 1
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username =  request.session['username'])
        environmentCate = EnviromentCate.objects.get(pk = idcate)
        subjects = Subject.objects.filter(enviromentcateid = environmentCate)
        arrRate = []
        for i in range(len(subjects)):
            arrRate.append(getrateSubject(subjects[i]))
        arrSubMas = []
        for i in range(len(subjects)):
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrRate[i][0],arrRate[i][1],converttimetoString(arrRate[i][2]),getlikeSubjectId(subjects[i]),enviromentcate.enviromentcatename)
            arrSubMas.append(temp)

        
        paginator = Paginator(arrSubMas, 9) 
        page = request.GET.get('page')
        arrSubMas = paginator.get_page(page)
        

        context = {
            'islog':islog,
            'environmentCate':environmentCate,
            'account':account,
            'arrSubMas':arrSubMas,
            'env': env,
        }
        return render(request, 'course/showsubjectcate.html', context)
    else:
        environmentCate = EnviromentCate.objects.get(pk = idcate)
        subjects = Subject.objects.filter(enviromentcateid = environmentCate)
        arrRate = []
        for i in range(len(subjects)):
            arrRate.append(getrateSubject(subjects[i]))
        arrSubMas = []
        for i in range(len(subjects)):
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrRate[i][0],arrRate[i][1],converttimetoString(arrRate[i][2]),getlikeSubjectId(subjects[i]),enviromentcate.enviromentcatename)
            arrSubMas.append(temp)
        
        paginator = Paginator(arrSubMas, 9) 
        page = request.GET.get('page')
        arrSubMas = paginator.get_page(page)
        

        context = {
            'islog':islog,
            'environmentCate':environmentCate,
            'arrSubMas':arrSubMas,
            'env': env,
        }
        return render(request, 'course/showsubjectcate.html', context)

def showsubjectsbyenvironment2(request):
    #  KT dang nhap
    env = 0
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username =  request.session['username'])
        environmentCate = EnviromentCate.objects.filter(enviromentcateid__gt=3)
        subjects = Subject.objects.filter(enviromentcateid__in = environmentCate)
        arrRate = []
        for i in range(len(subjects)):
            arrRate.append(getrateSubject(subjects[i]))
        arrSubMas = []
        for i in range(len(subjects)):
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrRate[i][0],arrRate[i][1],converttimetoString(arrRate[i][2]),getlikeSubjectId(subjects[i]),enviromentcate.enviromentcatename)
            arrSubMas.append(temp)

        
        paginator = Paginator(arrSubMas, 9) 
        page = request.GET.get('page')
        arrSubMas = paginator.get_page(page)
        

        context = {
            'islog':islog,
            'environmentCate':environmentCate,
            'account':account,
            'arrSubMas':arrSubMas,
            'env': env,
        }
        return render(request, 'course/showsubjectcate.html', context)
    else:
        environmentCate = EnviromentCate.objects.filter(enviromentcateid__gt=3)
        print(environmentCate)
        subjects = Subject.objects.filter(enviromentcateid__in = environmentCate)
        
        arrRate = []
        for i in range(len(subjects)):
            arrRate.append(getrateSubject(subjects[i]))
        arrSubMas = []
        for i in range(len(subjects)):
            subcate = subjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(subjects[i],arrRate[i][0],arrRate[i][1],converttimetoString(arrRate[i][2]),getlikeSubjectId(subjects[i]),enviromentcate.enviromentcatename)
            arrSubMas.append(temp)
        
        paginator = Paginator(arrSubMas, 9) 
        page = request.GET.get('page')
        arrSubMas = paginator.get_page(page)
        

        context = {
            'islog':islog,
            'environmentCate':environmentCate,
            'arrSubMas':arrSubMas,
            'env': env,
        }
        return render(request, 'course/showsubjectcate.html', context)


def dashboard(request):
    if request.session.has_key('username'):
        sum = 0
        account = Account.objects.get(username=request.session['username'])
        userdetail = UserDetail.objects.get(accountid = account)
        # Số lượng khóa học
        enrollments = Enrollment.objects.filter(accountid = account).order_by('createdate')
        arrDashs = []
        for enrollment in enrollments:
            sub = enrollment.subjectid
            countact=getCountActivity(sub)
            # Lấy số tracking trong 1 môn => số hd đã thuc hien
            trackings = Tracking.objects.filter(enrollmentid=enrollment).filter(subjectid = enrollment.subjectid)
            # Percent
            if countact != 0:
                percent = int((len(trackings)/countact)*100)
            else:
                percent = 0
            temp = ClassDashBoard(sub, countact,len(trackings),'width: ' + str(percent) + '%;')
            sum = sum +(len(trackings)*30)
            arrDashs.append(temp)
        level = getLevel(sum)
        rank = getRank(level.level)
        level.expperleft= 'width: ' + str(level.expperleft) + '%;'
        context={
            'rank':rank,
            'level':level,
            'arrDashs':arrDashs,
            'numEnroll':len(enrollments),
            'userdetail':userdetail,
            'account':account
        }
        return render(request, 'course/dashboard.html', context) 
    else:
        return redirect('homepage:index') 

def dashboardcourse(request, idsub):
    subject = Subject.objects.get(subjectid = idsub)
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        userdetail = UserDetail.objects.get(accountid = account)
        # Số lượng khóa học
        enrollments = Enrollment.objects.filter(accountid = account)
        # Tính phần trăm
        enrollment = enrollments.get(subjectid =subject)
        trackings = Tracking.objects.filter(enrollmentid=enrollment).filter(subjectid = enrollment.subjectid)
        percentSub = int((len(trackings)/getCountActivity(subject))*100) 
        percentSubhtml = 'width: ' + str(percentSub) + '%;'
        # Chapter trong 1 subject
        chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
        arrClassChap = []
        upAct = 1
        orderchap = 1
        orderles = 1
        for chapter in chapters:
            lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
            # Phần trăm chương
            trackings = Tracking.objects.filter(enrollmentid = enrollment).filter(chapterid = chapter)
            if getCountActivityInChapter(chapter) != 0:
                perChap = int((len(trackings)/getCountActivityInChapter(chapter))*100)
            else: 
                perChap = 0
            # Lay tong so activity trong lesson
            arrClassLess = []
            
            for lesson in lessons:
                activities = getActivityInLesson(lesson)
                arrClassAct = []
                actorder = 1
                actived = 0
                for activity in activities:
                    if boolcheckActivityTracking(activity, account) == 1:
                        t = 'activated'
                        actived += 1
                    else:
                        t = ''
                  
                    temp = ActDashBoard(activity, t, upAct)
                    arrClassAct.append(temp)
                    actorder +=1
                    upAct += 1
                if len(activities) != 0:
                    sumper = int((actived/actorder)*100)
                else: 
                    sumper = 0
                temp = LessonDashBoard(lesson, arrClassAct,'width: '+ str((1/actorder)*100) + '%;' ,'width: ' + str(sumper) + '%;', orderles)
                orderles += 1
                arrClassLess.append(temp)

            temp = ChapDashBoard(chapter,'width: ' + str(perChap) + '%;', arrClassLess, orderchap, perChap)
            orderchap += 1
            arrClassChap.append(temp)
       
        #Lay level
        sum=0
        for enrollment in enrollments:
            sub = enrollment.subjectid
            tracklevel = Tracking.objects.filter(enrollmentid=enrollment).filter(subjectid = enrollment.subjectid)
            sum = sum + (len(tracklevel)*30)
        level = getLevel(sum)
        rank = getRank(level.level)
        level.expperleft= 'width: ' + str(level.expperleft) + '%;'
        context={
            'rank':rank,
            'level':level,
            'chapters':chapters,
            'arrClassChap':arrClassChap,
            'percentSubhtml':percentSubhtml,
            'percentSub':percentSub,
            'subject':subject,
            'numEnroll':len(enrollments),
            'userdetail':userdetail,
            'account':account
        }
        return render(request, 'course/dashboardcourse.html', context) 
    else:
        return redirect('homepage:index') 

def courseoverview(request, idsub):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        subject = Subject.objects.get(subjectid = idsub)
        userdetail = UserDetail.objects.get(accountid=subject.accountid)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            chapters = Chapter.objects.filter(subjectid=subject).order_by('order')
            arrSpecials = []
            chapcount = 1
            lessoncount = 1
            for chapter in chapters:
                # Lấy lesson
                lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
                temp2 = []
                
                for lesson in lessons:
                    items = Item.objects.filter(lessonid = lesson).order_by('order')
                    itemcount = 1
                    temp1 = []
                    for item in items:
                        activities = Activity.objects.filter(itemid=item).order_by('order')
                        temp1.append(ItemAndActSimple(item,activities, itemcount))
                        itemcount +=1
                    temp2.append(LessAndItemSimple(lesson,temp1,lessoncount))
                    lessoncount += 1
                arrSpecials.append(ChapAndLessSimple(chapter, temp2, chapcount))
                chapcount += 1

            context = {
                'arrSpecials':arrSpecials,
                'userdetail':userdetail,
                'subject':subject,
                'account':account,
            }

            return render(request, 'course/courseoverview.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


# DELETE ACT, ITEM, LESSON, CHAP, SUBJECT
def deleteactivity(request, idact):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        activity = Activity.objects.get(activityid = idact)
        item = activity.itemid
        lesson = item.lessonid
        chapter = lesson.chapterid
        subject = chapter.subjectid
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            delActivity(activity)   
            return redirect('course:actinitem', idsub=subject.subjectid, idchap=chapter.chapterid, idles=lesson.lessonid, iditem=item.itemid)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def deleteitem(request, iditem):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        item = Item.objects.get(itemid = iditem)
        lesson = item.lessonid
        chapter = lesson.chapterid
        subject = chapter.subjectid
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            activities = Activity.objects.filter(itemid = item)
            for activity in activities:
                delActivity(activity)   
            
            numorder = item.order
            item.delete()
            items = Item.objects.filter(lessonid = lesson).order_by('order')

            for item in items:
                if item.order > numorder:
                    item.order = numorder - 1
                    item.save()

            return redirect('course:iteminles', idsub=subject.subjectid, idchap=chapter.chapterid, idles=lesson.lessonid)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index') 

def deletelesson(request, idles):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])  
        lesson = Lesson.objects.get(lessonid = idles)
        chapter = lesson.chapterid
        subject = chapter.subjectid
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            items = Item.objects.filter(lessonid = lesson).order_by('order')
            for item in items:
                activities = Activity.objects.filter(itemid = item).order_by('order')
                for activity in activities:
                    delActivity(activity)
            
                item.delete()
            
            numorder = lesson.order
            # Lesson Rep
            lessonreps = LessonReply.objects.filter(lessonid = lesson)
            for lessonrep in lessonreps:
                lessonrep.delete()

            lesson.delete()
            
            lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
            for lesson in lessons:
                if lesson.order > numorder:
                    lesson.order = lesson.order - 1
                    lesson.save()

            return redirect('course:lessinchap', idsub=subject.subjectid, idchap=chapter.chapterid)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def deletechapter(request, idchap):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username']) 
        chapter = Chapter.objects.get(chapterid = idchap)
        subject = chapter.subjectid
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            lessons = Lesson.objects.filter(chapterid=chapter).order_by('order')
            for lesson in lessons:
                items = Item.objects.filter(lessonid = lesson).order_by('order')
                for item in items:
                    activities = Activity.objects.filter(itemid = item).order_by('order')
                    for activity in activities:
                        delActivity(activity)    
                    item.delete()
                
                lessonreps = LessonReply.objects.filter(lessonid = lesson)
                for lessonrep in lessonreps:
                    lessonrep.delete() 
                lesson.delete()
            
            numorder = chapter.order
            chapter.delete()
            chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
            for chapter in chapters:
                if chapter.order > numorder:
                    chapter.order = chapter.order -1
                    chapter.save()

            return redirect('course:chapincourse', idsub=subject.subjectid)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def deletecourse(request, idsub):
    if request.session.has_key('username'):  
        account = Account.objects.get(username = request.session['username']) 
        subject = Subject.objects.get(subjectid = idsub)
        # Check phân quyền GV edit
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and boolcheckTeacherPermit(account, subject): 
            chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
            for chapter in chapters:
                lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
                for lesson in lessons:
                    items = Item.objects.filter(lessonid = lesson).order_by('order')
                    for item in items:
                        activities = Activity.objects.filter(itemid = item).order_by('order')
                        for activity in activities:
                            delActivity(activity)
                        item.delete()
                    # Lesson Rep
                    lessonreps = LessonReply.objects.filter(lessonid = lesson)
                    for lessonrep in lessonreps:
                        lessonrep.delete()
                    lesson.delete()
                chapter.delete()

            # Subject part
            # subparts = SubjectPart.objects.filter(subjectid = subject).order_by('order')
            # for subpart in subparts:
            #     subpart.delete()
            # Subject Like
            sublikes = SubjectLike.objects.filter(subjectid = subject)
            for sublike in sublikes:
                sublike.delete()
            # Enrollment
            enrolls = Enrollment.objects.filter(subjectid = subject)
            for enroll in enrolls:
                enroll.delete()
            # Teacher
            subteachers = SubjectTeacher.objects.filter(subjectid=subject)
            for subteacher in subteachers:
                subteacher.delete()

            subject.isenable = 3
            subject.save()

            return redirect('course:managecourse')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
		
def userforumcourse(request, idsub):
    islog = 0
    
    subject = Subject.objects.get(subjectid = idsub)
    forums = Forum.objects.filter(subjectid = idsub).order_by('-createdate')
    enviromentcate = EnviromentCate.objects.filter(enviromentcateid = subject.enviromentcateid.enviromentcateid)

    header = Header.objects.get(headername = 'Forum')

    userdetailforumlist = []
    for forum in forums:
        userdetail =  UserDetail.objects.get(accountid = forum.accountid)

        temp = ForumUserdetail(forum, userdetail)
        userdetailforumlist.append(temp)

    # Quy định cách hiển thị table forum khi chưa đăng nhập
    classdiv = "col-lg-12"

    #Chia trang
    # paginator = Paginator(userdetailforumlist, 10) # Show 25 contacts per page
    # page = request.GET.get('page')
    # userdetailforumlist = paginator.get_page(page)    


    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        # Quy định cách hiển thị table forum khi đã đăng nhập
        classdiv = "col-lg-9"

        # Kiểm tra xem người dùng đã đăng ký môn học chưa
        if boolcheckEnroll(subject, request.session['username']):
            # load các bài viết của user
            yourforums = Forum.objects.filter(subjectid=idsub).filter(accountid = account.accountid).order_by('-createdate')
            lenyourfor = len(yourforums)
            if lenyourfor >4:
                yourforums = yourforums[0:4]

            # load các bài viết mà user tương tác
            forumreplys = ForumReply.objects.filter(accountid = account.accountid).order_by('-createdate')
            lenforrep = len(forumreplys)
            if lenforrep >4:
                forumreplys = forumreplys[0:4]

            context = {
                'islog': islog,
                'account':account,
                'enviromentcate': enviromentcate,
                'subject': subject,
                'forums': forums,
                'userdetailforumlist': userdetailforumlist,
                'yourforums': yourforums,
                'forumreplys': forumreplys,
                'classdiv': classdiv,
                'header': header,
            }
            return render(request, 'course/userforumcourse.html', context)
        else:
            return redirect('homepage:index')

    return redirect('homepage:index')

    
def userforumpostcourse(request, idsub):
    islog = 0
    subject = Subject.objects.get(subjectid = idsub)

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        enviromentcates = EnviromentCate.objects.all()

        if request.method == "POST":
            # enviromentcateid = request.POST.get('enviromentcateid')
            enviromentcateid = subject.enviromentcateid
            forumtopicname = request.POST.get('forumtopicname')
            content = request.POST.get('content')
            try:
                avatar = request.FILES.get('avatar')
            except:
                avatar = None
            if avatar != None:
                ava = tokenFile(avatar)
            else:
                ava = ''
            note = request.POST.get('note')

            forum = Forum(
                enviromentcateid = enviromentcateid,
                accountid = account,
                subjectid = subject,
                forumtopicname = forumtopicname,
                content = content,
                createdate = datetime.now(),
                editdate = datetime.now(),
                avatar = ava,
                viewcount = 0,
                likecount = 0,
                isenable = 1,
                note = note,
            )
            forum.save()

            context = {
            'islog': islog,
            'account':account,
            'subject': subject,
            'enviromentcates': enviromentcates,
            }
            return redirect('course:userforumcourse', idsub=subject.subjectid)

        context = {
            'islog': islog,
            'account':account,
            'subject': subject,
            'enviromentcates': enviromentcates,
        }
        return render(request, 'course/userforumpostcourse.html', context)
    else:  
        context = {
            'islog': islog,
            'subject': subject,
        }
        return redirect('homepage:index')


def userforumblogcourse(request, idsub, idfor):
    islog = 0
    forum = Forum.objects.get(forumtopicid = idfor)
    subject = Subject.objects.get(subjectid = idsub)

    forum.viewcount +=1
    forum.save()

    like = 0
    likeCount = getlikeForumId(forum)

    forumreplys = ForumReply.objects.filter(forumtopicid = forum).order_by('-createdate')
    userdetailforumreplylist = []
    for forumreply in forumreplys:
        forumreply.forumreplyid = 'CommentDelete(' + str(forumreply.forumreplyid) + ')'
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        temp = ForumReplyUserdetail(forumreply, userdetail)
        userdetailforumreplylist.append(temp)
    lenforumreplys = len(forumreplys)

    popularforums = Forum.objects.filter(subjectid = subject).order_by('-viewcount')
    popularforums = popularforums[0:4]

    relativeforums = Forum.objects.filter(subjectid = subject).filter(enviromentcateid = forum.enviromentcateid).order_by('-createdate')
    relativeforums = relativeforums[0:4]

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        
        usename = request.session['username']
        if checkLikeForum(idfor, usename):
            like = 1

        context = {
            'islog': islog,
            'forum': forum,
            'account':account,
            'subject':subject,
            'userdetailforumreplylist': userdetailforumreplylist,
            'forumreplys': forumreplys,
            'lenforumreplys': lenforumreplys,
            'popularforums': popularforums,
            'relativeforums': relativeforums,
            'likeCount': likeCount,
            'like': like,
        }
    
        return render(request, 'course/userforumblogcourse.html', context)

    context = {
        'forum': forum,
        'islog': islog,
        'subject':subject,
        'userdetailforumreplylist': userdetailforumreplylist,
        'forumreplys': forumreplys,
        'lenforumreplys': lenforumreplys,
        'popularforums': popularforums,
        'relativeforums': relativeforums,
        'likeCount': likeCount,
            'like': like,
    }
    return render(request, 'course/userforumblogcourse.html', context)

def allcourse(request):
    searchsubjects = Subject.objects.all().order_by('-createdate')
    show = 1
    # KT dang nhap
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username=request.session['username'])

        if len(searchsubjects) == 0:
            context={
                    'show':0,
                    'islog':islog,
                    'account':account,
            }
            return render(request, 'homepage/listsubject.html', context)
        # Lấy mảng rate
        arrSub = []
        for i in range(len(searchsubjects)):
            arrSub.append(getrateSubject(searchsubjects[i]))
        # Tạo mảng có biến class SubjectMaster
        arrSubM = []
        for i in range(len(searchsubjects)):
            # Lấy cate
            subcate = searchsubjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(searchsubjects[i],arrSub[i][0],arrSub[i][1],converttimetoString(arrSub[i][2]),getlikeSubjectId(searchsubjects[i]), enviromentcate.enviromentcatename)
            arrSubM.append(temp)
            
            
        paginator = Paginator(arrSubM, 10) 
        page = request.GET.get('page')
        arrSubM = paginator.get_page(page)


        context={
                'arrSubM':arrSubM,
                'show':show,
                'islog':islog,
                'account':account,
            }
        return render(request, 'homepage/listsubject.html', context)
    else:
        islog = 0
        if len(searchsubjects) == 0:
            context={
                    'show':0,
                    'islog':islog,
            }
            return render(request, 'homepage/listsubject.html', context)
        # Lấy mảng rate
        arrSub = []
        for i in range(len(searchsubjects)):
            arrSub.append(getrateSubject(searchsubjects[i]))
        # Tạo mảng có biến class SubjectMaster
        arrSubM = []
        for i in range(len(searchsubjects)):
            # Lấy cate
            subcate = searchsubjects[i].enviromentcateid
            enviromentcate = EnviromentCate.objects.get(enviromentcateid = subcate.enviromentcateid)
            temp = SubjectMaster(searchsubjects[i],arrSub[i][0],arrSub[i][1],converttimetoString(arrSub[i][2]),getlikeSubjectId(searchsubjects[i]), enviromentcate.enviromentcatename)
            arrSubM.append(temp)
            
        paginator = Paginator(arrSubM, 10) 
        page = request.GET.get('page')
        arrSubM = paginator.get_page(page)

        context={
                'arrSubM':arrSubM,
                'show':show,
                'islog':islog,
            }
        return render(request, 'homepage/listsubject.html', context)
        
def mblock(request):
     return render(request, 'course/mblock.html')



