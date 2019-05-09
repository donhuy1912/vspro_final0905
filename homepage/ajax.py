from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from datetime import datetime, date, time

def ajaxLike(request):
    subid = request.GET.get("subid", None)
    subject = Subject.objects.get(subjectid = subid)
    
    username = request.session['username']
    account = Account.objects.get(username=username)
        
    subjectlike = SubjectLike(
                                accountid = Account.objects.get(accountid = account.accountid),
                                subjectid = subject,
                                status = 1,
                                isenable = 1,
        )
    subjectlike.save()

    sublikes = SubjectLike.objects.filter(subjectid = subid)
    likecount = len(sublikes)
    data = {
        'likecount':likecount
    }

    return JsonResponse(data)

def ajaxUnlike(request):
    subid = request.GET.get("subid", None)
    username = request.session["username"]
    acc = Account.objects.get(username=username)
    sublike =  SubjectLike.objects.filter(accountid=acc.accountid).filter(subjectid = subid)
    sublike.delete()
    sublikes = SubjectLike.objects.filter(subjectid = subid)
    likecount = len(sublikes)
    data = {
        'likecount': likecount
    }
    return JsonResponse(data)

def ajaxChapContent(request):
    chapid = request.GET.get("chapid", None)
    chapter = Chapter.objects.get(chapterid = chapid)
    chapterName = chapter.chaptername
    chapterContent = chapter.content
    chapterName = 'BÀI ' + str(chapter.order) + ': ' + chapter.chaptername
    data = {
        'chapterName': chapterName,
        'chapterContent':chapterContent,
    }
    return JsonResponse(data)

def ajaxDelCommentLes(request):
    lesrepid = request.GET.get("lesrepid", None)
    lesReply = LessonReply.objects.get(lessonreplyid=lesrepid)
    # lấy id lesson
    lesid = lesReply.lessonid.lessonid
    # xóa lesReply
    lesReply.delete()
    # load lại lesrep
    lessonreplies = LessonReply.objects.filter(lessonid = lesid).order_by('-createdate')
    s = ''
    temp = ''
    for lessonreply in lessonreplies:
        enrollment = lessonreply.enrollmentid
        acc = enrollment.accountid
        delbut=''
        if acc.username == request.session['username']:
            delbut='''<br><br> <a  onclick=check('''+str(lessonreply.lessonreplyid)+''') class="btn_1" style="background-color:#FFC107;color:white">Xóa</a>'''
        temp = '''<div id="listcmt" class="review-box clearfix">			
										<figure class="rev-thumb"><img src="'''+acc.avatar +'''" alt="" style="width:40px;height:40px;border-radius:50%;display:inline" >
										</figure>
										<div class="rev-content">
												<div class="rev-info">
												'''	+ acc.username + ''' - ''' + str(lessonreply.createdate) + delbut +'''
												</div>
												
												<div class="rev-text">
													<p>
														'''+ lessonreply.content+ '''
													</p>
												</div>
											</div>
									</div>'''
        s += temp
    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxDelCommentActRep(request):
    actRepId = request.GET.get("idactRep", None)
    # Lấy activityReply
    actRep = ActivityReply.objects.get(activityreplyid=actRepId)
    # Lấy activity
    activity = actRep.activityid
    # Xóa activityReply
    actRep.delete()
    # Load activityRep
    activityReplies = ActivityReply.objects.filter(activityid=activity).order_by('-createdate')
    s = ''
    temp = ''
    for activityReply in activityReplies:
        enrollment = activityReply.enrollmentid
        acc = enrollment.accountid
        delbut=''
        rate=''
        for i in range(5):
            if i < activityReply.rate:
                rate+='''<i class="icon_star voted"></i>'''
            else:
                rate+='''<i class="icon_star"></i>'''
        if acc.username == request.session['username']:
            delbut='''<br><br> <a  onclick=check('''+ str(activityReply.activityreplyid)+''') class="btn_1" style="background-color:#FFC107;color:white">Xóa</a>'''
        temp = '''
                                    <div id="listcmt">
									<div  class="review-box clearfix">
										<figure class="rev-thumb"><img src="'''+ acc.avatar +'''" alt="" style="width:40px;height:40px;border-radius:50%;display:inline" >
										</figure>
										<div class="rev-content">
											<div class="rating">
											'''+ rate +'''	
											</div>
												<div class="rev-info">
												'''+ acc.username +''' - '''+ str(activityReply.createdate.date()) + delbut + '''
												</div>
												
												<div class="rev-text">
													<p>
														'''+ activityReply.content +'''
													</p>
												</div>
											</div>
									</div>
                                    </div>

        '''
        s += temp
    data = {
        's':s
    }
    return JsonResponse(data)

def ajaxtrackingActivity(request):
    actid = request.GET.get('actid',None)
    activity = Activity.objects.get(activityid = actid)
    item = activity.itemid
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject = chapter.subjectid
    # Lưu tracking
    account = Account.objects.get(username = request.session['username'])
    enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject)

    # kiem tra da luu tracking chua
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

    # Lay HD tiep theo
    nextActs = Activity.objects.filter(itemid = item).order_by('order')
    getAct = ''
    for nexAct in nextActs:
        if nexAct.order > activity.order:
            getAct = nexAct
            break
    if getAct == '':
        s = "Bạn đã hoàn thành tất cả hoạt động của :" + item.itemname
        link=''
        data= {
            's': s,
            'link':link
        }
        return JsonResponse(data)
    else:
        s = 'Đi đến hoạt động kế tiếp'
        # linknextAct = """{% url 'course:courseactivity' idsub="""+ str(subject.subjectid) + """ idchap="""+ str(chapter.chapterid)+ """ idles="""+ str(lesson.lessonid)+ """ iditem=""" +str(item.itemid)+ """ idact="""+str(getAct.activityid)+ """ %}"""
        data= {
            's': s,
            'link': str(getAct.activityid)
        }
        return JsonResponse(data)

def ajaxCreateCommentActRep(request):

    idact = request.GET.get("idact", None)
    rate = request.GET.get("rate", None)
    des = request.GET.get("des", None)
    activity = Activity.objects.get(activityid =  idact)
    # subid
    item = activity.itemid
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject = chapter.subjectid

    account = Account.objects.get(username = request.session['username'])
    enrollment = Enrollment.objects.filter(accountid = account).get(subjectid = subject)
    
    actRep = ActivityReply(
        enrollmentid = enrollment,
        activityid = activity,
        content = des,
        createdate = datetime.now(),
        editdate = datetime.now(),
        rate = rate,
        isenable = 1,
        note = '',
    )
    actRep.save()
    
    # Load activityRep
    activityReplies = ActivityReply.objects.filter(activityid=activity).order_by('-createdate')
    s = ''
    temp = ''
    for activityReply in activityReplies:
        enrollment = activityReply.enrollmentid
        acc = enrollment.accountid
        delbut=''
        rate=''
        for i in range(5):
            if i < activityReply.rate:
                rate+='''<i class="icon_star voted"></i>'''
            else:
                rate+='''<i class="icon_star"></i>'''
        if acc.username == request.session['username']:
            delbut='''<br><br> <a  onclick=check('''+ str(activityReply.activityreplyid)+''') class="btn_1" style="background-color:#FFC107;color:white">Xóa</a>'''
        temp = '''
                                    <div id="listcmt">
									<div  class="review-box clearfix">
										<figure class="rev-thumb"><img src="'''+ acc.avatar +'''" alt="" style="width:40px;height:40px;border-radius:50%;display:inline">
										</figure>
										<div class="rev-content">
											<div class="rating">
											'''+ rate +'''	
											</div>
												<div class="rev-info">
												'''+ acc.username +''' - '''+ str(activityReply.createdate.date()) + delbut + '''
												</div>
												
												<div class="rev-text">
													<p>
														'''+ activityReply.content +'''
													</p>
												</div>
											</div>
									</div>
                                    </div>

        '''
        s += temp
    data = {
        's':s
    }
    return JsonResponse(data)

def ajaxSortChap(request):
    orderT = request.GET.get('order', None)
    chapidT = request.GET.get('chapid', None)
    idsub = request.GET.get('idsub', None)
    # sort
    subject=Subject.objects.get(subjectid=idsub)
    if subject.isenable == 0:
        chapter = Chapter.objects.get(chapterid = chapidT)
        chapter.order = orderT
        chapter.save()
        color="#76ff3f"
        alert= "Thành Công"
    else:
        alert="Khóa Học Đã Được Phát Hành Không Thể Chỉnh Sửa Thứ Tự"
        
        color="#ff3f7c"
    data = {
        'alert':alert,
        'color':color
    }
    return JsonResponse(data)

def ajaxAfterSortChap(request):
    idsub = request.GET.get('idsub',None)
    subject = Subject.objects.get(subjectid = idsub)
    chapters = Chapter.objects.filter(subjectid = subject).order_by('order')
    
    i = 1
    s = ''
    for chap in chapters:
        chap.chaptername = 'Bài ' + str(i) + ': ' + chap.chaptername
        i += 1
        linktq = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chap.chapterid) + "/edit"
        linknd = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chap.chapterid)
        linkx = "/chapter/" + str(chap.chapterid) + "/delete/"
        temp='''<li class="sort" id="'''+ str(chap.chapterid)+'''">
                      <div class="x_panel" style="width: 100%;height:auto;box-shadow: 5px 10px 8px #888888;background: url(/media/Kidprogram.png)">
                          <div class="x_title">
                              <h2 style="font-size: 1.8em; color: #ff0066; text-align: center; font-family: 'Marvel', sans-serif;"> '''+ chap.chaptername +'''</h2>
                              <ul class="nav navbar-right panel_toolbox">
                              <li><a href='''+ linktq +''' ><i class="fa fa-edit" style="font-size:13.5pt;color:#800080;">Tổng quan</i></a></li>
                              <li><a href='''+ linknd +''' ><i class="fa fa-gears" style="font-size:13.5pt;color:#800080;"> Nội dung</i></a></li>
                               <li><a href='''+ linkx +''' ><i class="fa fa-trash" style="font-size:13.5pt;color:#800080;"> Xóa</i></a></li>
                             
                              </li>
                              <li class="dropdown">
                              </li>
                              <li>
                              </li>
                              
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                          
                        </div>
                  </li>'''
        s += temp

    data = {
        's' : s
    }
    return JsonResponse(data)

def ajaxSortLes(request):
    orderT = request.GET.get('order', None)
    lesid = request.GET.get('lesid', None)
    # sort
    lesson = Lesson.objects.get(lessonid = lesid)
    lesson.order = orderT
    lesson.save()
    data = {
    }
    return JsonResponse(data)

def ajaxAfterSortLes(request):
    idchap = request.GET.get('idchap',None)
    chapter = Chapter.objects.get(chapterid = idchap)
    lessons = Lesson.objects.filter(chapterid = chapter).order_by('order')
    subject=chapter.subjectid
    i = 1
    s = ''
    for lesson in lessons:
        lesson.lessonname = 'Chủ đề ' + str(i) + ': ' + lesson.lessonname
        linktq = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid)+"/lesson/"+str(lesson.lessonid) + "/edit"
        linknd = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid) + "/lesson/" + str(lesson.lessonid) + "/iteminles"
        linkx = "/lesson/" + str(lesson.lessonid) + "/delete/"
        # course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/iteminles
        i += 1
        temp='''<li class="sort" id="'''+ str(lesson.lessonid)+'''">
                      <div class="x_panel" style="width: 100%;height:auto;box-shadow: 5px 10px 8px #888888;background: url(/media/Kidprogram.png)">
                          <div class="x_title">
                              <h2 style="font-size: 1.8em; color: #ff0066; text-align: center; font-family: 'Marvel', sans-serif;"> '''+ lesson.lessonname +'''</h2>
                              <ul class="nav navbar-right panel_toolbox">
                              <li><a href= '''+ linktq  +''' ><i class="fa fa-edit" style="font-size:13.5pt;color:#800080;">Tổng quan</i></a>
                              <li><a href= '''+ linknd  +'''><i class="fa fa-gears" style="font-size:13.5pt;color:#800080;"> Nội dung</i></a>
                             <li><a href= '''+ linkx  +''' ><i class="fa fa-trash" style="font-size:13.5pt;color:#800080;"> Xóa</i></a>
                              
                              </li>
                              <li class="dropdown">
                              </li>
                              <li>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                          
                        </div>
                  </li>'''
        s += temp

    data = {
        's' : s
    }
    return JsonResponse(data)

def ajaxSortItem(request):
    orderT = request.GET.get('order', None)
    itemid = request.GET.get('itemid', None)
    # sort
    item = Item.objects.get(itemid = itemid)
    item.order = orderT
    item.save()
    data = {
    }
    return JsonResponse(data)

def ajaxAfterSortItem(request):
    lesid = request.GET.get('lesid',None)
    lesson = Lesson.objects.get(lessonid=lesid)
    items = Item.objects.filter(lessonid = lesson).order_by("order")
    chapter = lesson.chapterid
    subject= chapter.subjectid
    i = 1
    s = ''
    for item in items:
        item.itemname =  str(i) + '/' + item.itemname
        linktq = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid)+"/lesson/"+str(lesson.lessonid) + '/item/'+ str(item.itemid) + "/edit"
        linknd = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid) + "/lesson/" + str(lesson.lessonid) + "/iteminles"
        linkx = "/item/" + str(item.itemid) + "/delete/"
        # course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/iteminles
        i += 1
        temp='''<li class="sort" id="'''+ str(item.itemid)+'''">
                      <div class="x_panel" style="width: 100%;height:auto;box-shadow: 5px 10px 8px #888888;background: url(/media/Kidprogram.png)">
                          <div class="x_title">
                              <h2 style="font-size: 1.8em; color: #ff0066; text-align: center; font-family: 'Marvel', sans-serif;"> '''+ item.itemname +'''</h2>
                              <ul class="nav navbar-right panel_toolbox">
                              <li><a href= '''+ linktq  +''' ><i class="fa fa-edit" style="font-size:13.5pt;color:#800080;">Tổng quan</i></a>
                              <li><a href= ''' + linknd + '''><i class="fa fa-gears" style="font-size:13.5pt;color:#800080;"> Nội dung</i></a>
                             <li><a href= '''+ linkx  +''' ><i class="fa fa-trash" style="font-size:13.5pt;color:#800080;"> Xóa</i></a>
                             
                              </li>
                              <li class="dropdown">
                              </li>
                              <li>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                          
                        </div>
                  </li>'''
        s += temp

    data = {
        's' : s
    }
    return JsonResponse(data)

def ajaxSortAct(request):
    orderT = request.GET.get('order', None)
    actid = request.GET.get('actid', None)
    # sort
    activity = Activity.objects.get(activityid = actid)
    activity.order = orderT
    activity.save()
    data = {
    }
    return JsonResponse(data)

def ajaxAfterSortAct(request):
    iditem = request.GET.get('iditem',None)
    item = Item.objects.get(itemid = iditem)
    activities = Activity.objects.filter(itemid = item).order_by("order")
    lesson = item.lessonid
    chapter = lesson.chapterid
    subject= chapter.subjectid
    i = 1
    s = ''
    for activity in activities:
        activity.activityname = 'Hoạt động ' + str(i) + ': ' + activity.activityname
        linktq = ''
        linktq = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid)+"/lesson/"+str(lesson.lessonid) + '/item/'+ str(item.itemid) + "/edit"
        linkx = "/activity/" + str(activity.activityid) + "/delete/"
        
        # linknd = "/course/"+ str(subject.subjectid) +"/chapter/" + str(chapter.chapterid) + "/lesson/" + str(lesson.lessonid) + "/iteminles"
        # course/<int:idsub>/chapter/<int:idchap>/lesson/<int:idles>/iteminles
        i += 1
        temp='''<li class="sort" id="'''+ str(activity.activityid)+'''">
                      <div class="x_panel" style="width: 100%;height:auto;box-shadow: 5px 10px 8px #888888;background: url(/media/Kidprogram.png)">
                          <div class="x_title">
                              <h2 style="font-size: 1.8em; color: #ff0066; text-align: center; font-family: 'Marvel', sans-serif;"> '''+ activity.activityname +'''</h2>
                              <ul class="nav navbar-right panel_toolbox">
                              <li><a href= '''+ linktq  +''' ><i class="fa fa-edit" style="font-size:13.5pt;color:#800080;">Tổng quan</i></a>
                                <li><a href= '''+ linkx  +''' ><i class="fa fa-trash" style="font-size:13.5pt;color:#800080;"> Xóa</i></a>
                             
                              <li class="dropdown">
                              </li>
                              <li>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                         
                        </div>
                  </li>'''
        s += temp

    data = {
        's' : s
    }
    return JsonResponse(data)

def ajaxchecktypeact(request):
    iptypeact = request.GET.get('iptypeact', None)
    flag = True
    try:
        acttype = ActivityType.objects.filter(activitytypeid = iptypeact)
        if (len(acttype) != 0):
            flag = True
        else:flag = False
    except:
        flag = False
    
    data = {
        'flag':flag
    }
    return JsonResponse(data)

def ajaxcheckenvir(request):
    ipenvir = request.GET.get('ipenvir', None)
    flag = True
    try:
        envir = EnviromentCate.objects.filter(enviromentcateid = ipenvir)
        if (len(envir) != 0):
            flag = True
        else:flag = False
    except:
        flag = False
    
    data = {
        'flag':flag
    }
    return JsonResponse(data)

def ajaxcheckactivityreq(request):
    ipreq = request.GET.get('ipreq', None)
    idact = request.GET.get('idact', None)
    activity = Activity.objects.get(activityid = idact)
    activityreq = Activity.objects.get(activityid = ipreq)

    item = activity.itemid
    lesson = item.lessonid
    
    itemreq=activityreq.itemid
    lessonreq = itemreq.lessonid
    if lesson.lessonid == lessonreq.lessonid or ipreq=="NULL":
        flag=True
    else:
        flag=False
    data = {
        'flag':flag
    }
    return JsonResponse(data)

def ajaxcheckactivityreqcreate(request):
    ipreq = request.GET.get('ipreq', None)
    iditem = request.GET.get('iditem', None)
    activityreq = Activity.objects.get(activityid = ipreq)

    item = Item.objects.get(itemid=iditem)
    lesson = item.lessonid
    
    itemreq=activityreq.itemid
    lessonreq = itemreq.lessonid
    if lesson.lessonid == lessonreq.lessonid or ipreq=="NULL":
        flag=True
    else:
        flag=False
    data = {
        'flag':flag
    }
    return JsonResponse(data)

# Thiết đặt sự kiện cho thanh Tìm kiếm Diễn đàn
def ajaxSearchForCourse(request):
    forname = request.GET.get('forname', None)
    subjectid = request.GET.get('subjectid')
    check = request.GET.get('check', None)
    # enviromentcate = request.GET.get('enviromentcate', None)
    if forname == None or forname == '':
        if check == '2':
            searchforums = Forum.objects.filter(subjectid = subjectid).order_by('-viewcount') 
        else:
            searchforums = Forum.objects.filter(subjectid = subjectid).order_by('-createdate')
        
        userdetailforumlist = []
        s = ''
        for searchforum in searchforums:
            userdetail =  UserDetail.objects.get(accountid = searchforum.accountid)
            temp = ForumUserdetail(searchforum, userdetail)
            userdetailforumlist.append(temp)
    else:
        if check == '2':
            searchforums = Forum.objects.filter(subjectid = subjectid).filter(forumtopicname__icontains = forname).order_by('-viewcount') # icontains: tìm kiếm gần đúng           
        else:
            searchforums = Forum.objects.filter(subjectid = subjectid).filter(forumtopicname__icontains = forname).order_by('-createdate') # icontains: tìm kiếm gần đúng
        s = ''
        userdetailforumlist = []
        for searchforum in searchforums:
            userdetail =  UserDetail.objects.get(accountid = searchforum.accountid)
            temp = ForumUserdetail(searchforum, userdetail)
            userdetailforumlist.append(temp)

    for userforlist in userdetailforumlist:
        linkforumblog = '/course/' + str(subjectid) + '/userforumblogcourse/' + str(userforlist.forum.forumtopicid) + '/'
        if userforlist.forum.avatar != None:
            img = '<img src="'  + str(userforlist.forum.avatar) + '" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
        else:
            img = '<img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
		
        s += '<tr><td class="options" style="width:5%; text-align:center;"><div class="thumb_cart" style = "border-radius: 50%">'
        s += img + '</div></td>'
        s += '<td><span class="options" ><a href="' + linkforumblog + '">' + str(userforlist.forum.forumtopicname) + '</a></span></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.userdetail.lastname) + ' ' + str(userforlist.userdetail.firstname) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.createdate.day) + '-' + str(userforlist.forum.createdate.month) + '-' + str(userforlist.forum.createdate.year) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.viewcount) + '</strong></td></tr>'

    data= {
       'is_taken': s,
    }

    return JsonResponse(data)

# Load dữ liệu theo tab All/Popular và Enviromentcate
def ajaxShowForCourse(request):
    check = request.GET.get('check', None)
    # enviromentcate = request.GET.get('enviromentcate', None)
    subjectid = request.GET.get('subjectid', None)
    if check == '2':
        searchforums = Forum.objects.filter(subjectid = subjectid).order_by('-viewcount')
    else:
        searchforums = Forum.objects.filter(subjectid = subjectid).order_by('-createdate')
        
    userdetailforumlist = []
    s = ''
    for searchforum in searchforums:
        userdetail =  UserDetail.objects.get(accountid = searchforum.accountid)
        temp = ForumUserdetail(searchforum, userdetail)
        userdetailforumlist.append(temp)
    
    for userforlist in userdetailforumlist:
        linkforumblog = '/course/' + str(subjectid) + '/userforumblogcourse/' + str(userforlist.forum.forumtopicid) + '/'
        if userforlist.forum.avatar != None:
            img = '<img src="'  + str(userforlist.forum.avatar) + '" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
        else:
            img = '<img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt="Image" style="width:40px;height:40px;border-radius:50%;display:inline">'
		
        s += '<tr><td class="options" style="width:5%; text-align:center;"><div class="thumb_cart" style = "border-radius: 50%">'
        s += img + '</div></td>'
        s += '<td><span class="options" ><a href="' + linkforumblog + '">' + str(userforlist.forum.forumtopicname) + '</a></span></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.userdetail.lastname) + ' ' + str(userforlist.userdetail.firstname) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.createdate.day) + '-' + str(userforlist.forum.createdate.month) + '-' + str(userforlist.forum.createdate.year) + '</strong></td>'
        s += '<td class="options" style="width:5%; text-align:center;"><strong>' + str(userforlist.forum.viewcount) + '</strong></td></tr>'

    data= {
       'is_taken': s,
    }

    return JsonResponse(data)

# Xóa ForumReply
def ajaxDelCommentForCourse(request):
    forumreplyid = request.GET.get("forumreplyid", None)
    subjectid = request.GET.get('subjectid', None)

    # Lấy forumreply
    forumreply = ForumReply.objects.get(forumreplyid=forumreplyid)
    # Lấy forumtopicid
    forumtopicid =  forumreply.forumtopicid
    
    # Xóa forumreply
    forumreply.delete()
    # Load forumreply
    forumreplys = ForumReply.objects.filter(forumtopicid= forumtopicid).order_by('-createdate')
    s = ''
    temp = ''
    for forumreply in forumreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        delbut=''
        if forumreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(forumreply.forumreplyid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        if forumreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(forumreply.accountid.avatar) + '" style="width:68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(forumreply.createdate.day) + '-' + str(forumreply.createdate.month) + '-' + str(forumreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(forumreply.content) + '</div></li>'
												
        s += temp
    data = {
        's': s
    }
    return JsonResponse(data)

# Tạo ForumReply
def ajaxCreateCommentForCourse(request):
    accountid = request.GET.get('accountid', None)
    forumtopicid = request.GET.get("forumtopicid", None)
    subjectid = request.GET.get('subjectid', None)
    content = request.GET.get("content", None)
    forum = Forum.objects.get(forumtopicid =  forumtopicid)
    

    account = Account.objects.get(accountid = accountid)
    subject = Subject.objects.get(subjectid = subjectid)
    
    forumreply = ForumReply(
        accountid = account,
        forumtopicid = forum,
        content = content,
        createdate = datetime.now(),
        editdate = datetime.now(),
        isenable = 1,
        note = '',
    )
    forumreply.save()
    
    # Load forumreplys
    forumreplys = ForumReply.objects.filter(forumtopicid= forumtopicid).order_by('-createdate')
    s = ''
    temp = ''
    for forumreply in forumreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        delbut=''
        if forumreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(forumreply.forumreplyid) + ',' + str(subjectid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        
        if forumreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(forumreply.accountid.avatar) + '" style="width:68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(forumreply.createdate.day) + '-' + str(forumreply.createdate.month) + '-' + str(forumreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(forumreply.content) + '</div></li>'
												
        s += temp
    data = {
        's': s
    }
    return JsonResponse(data)

# Load Bình Luận cho Forum (gồm xóa và tạo cmt)
def ajaxShowCommentForCourse(request):
    accountid = request.GET.get('accountid', None)
    forumtopicid = request.GET.get("forumtopicid", None)
    content = request.GET.get("content", None)
    forum = Forum.objects.get(forumtopicid =  forumtopicid)
    account = Account.objects.get(accountid = accountid)
    page = request.GET.get('page', None)
    delforcmt = request.GET.get('delforcmt', None)
    creforcmt = request.GET.get('creforcmt', None)
    subjectid = request.GET.get('subjectid', None)

    subject = Subject.objects.get(subjectid = subjectid)

    if page == None or page == '':
        page = 0
    else:
        page = int(page)

    forumreplyid = request.GET.get("forumreplyid", None)

    if forumtopicid == None or forumtopicid == '':
        pass
    else:
        forumtopicid = int(forumtopicid)

    if forumreplyid == None or forumreplyid == '':
        pass
    else:
        forumreplyid = int(forumreplyid)

    if delforcmt == '1':
        # Lấy forumreply
        forumreply = ForumReply.objects.get(forumreplyid=forumreplyid)
        # Lấy forumtopicid
        forumtopicid =  forumreply.forumtopicid
        # Xóa forumreply
        forumreply.delete()

    if creforcmt == '1':
        forumreply = ForumReply(
            accountid = account,
            forumtopicid = forum,
            content = content,
            createdate = datetime.now(),
            editdate = datetime.now(),
            isenable = 1,
            note = '',
        )
        forumreply.save()
   
    
    # Load forumreplys
    forumreplys = ForumReply.objects.filter(forumtopicid= forumtopicid).order_by('-createdate')

    btnmore = 1
    first = 4*page
    last = (page+1)*4
    if len(forumreplys) < last:
        last = len(forumreplys)
        btnmore = 0
    if first >= len(forumreplys):
        forumreplys = []
    else:
        forumreplys = forumreplys[first:last]

    s = ''
    temp = ''
    for forumreply in forumreplys:
        temp = ''
        userdetail = UserDetail.objects.get(accountid = forumreply.accountid)
        delbut=''
        if forumreply.accountid.username == request.session['username']:
            delbut='&nbsp<button  onclick= CommentDelete(' + str(forumreply.forumreplyid) + ',' + str(subjectid) + ') class="" style="background-color:#FFC107; color:white; border-radius: 30%">Xóa</button>'
        
        img = ''
        
        if forumreply.accountid.avatar != None:
            img = '<a href="#"><img src="' + str(forumreply.accountid.avatar) + '" style="width:68px; height:68px" alt=""></a>'
        else:
            img = '<a href="#"><img src="http://via.placeholder.com/150x150/ccc/fff/avatar1.jpg" alt=""></a>'

        temp += '<li><div class="avatar">' + img + '</div><div class="comment_right clearfix"><div class="comment_info">'
        temp += 'Bình luận của <a href="#">' + str(userdetail.lastname) + ' ' + str(userdetail.firstname) + '</a><span>|</span>' + str(forumreply.createdate.day) + '-' + str(forumreply.createdate.month) + '-' + str(forumreply.createdate.year) + '<span>|'
        temp += delbut + '</span></div>' + str(forumreply.content) + '</div></li>'
												
        s += temp
        
    data = {
        's': s,
        'btnmore': btnmore,
        'page':page,
    }
    return JsonResponse(data)

def ajaxmanagecourseenvir(request):
    envir = request.GET.get('envir', None)
    page = request.GET.get('page', None)
    account = Account.objects.get(username = request.session['username'])
    if page =='':
        page=0
    else:
        page=int(page)
    envir = int(envir)
    if envir != 0:
        subjects1QR = Subject.objects.filter(accountid = account).exclude(isenable=3).filter(enviromentcateid = envir).order_by('-createdate')
        subjects1 = []
        for subject1QR in subjects1QR:
            subjects1.append(subject1QR)
        subjectteachers2 = SubjectTeacher.objects.filter(accountid = account)
        subjects2 = []
        for subjectteacher2 in subjectteachers2:
            if subjectteacher2.subjectid.enviromentcateid == envir:
                subjects2.append(subjectteacher2.subjectid)
        subjects = subjects1 + subjects2
    else:
        subjects1QR = Subject.objects.filter(accountid = account).order_by('-createdate')
        subjects1 = []
        for subject1QR in subjects1QR:
            subjects1.append(subject1QR)
        subjectteachers2 = SubjectTeacher.objects.filter(accountid = account)
        subjects2 = []
        for subjectteacher2 in subjectteachers2:
            subjects2.append(subjectteacher2.subjectid)
        subjects = subjects1 + subjects2
    btnmore = 1
    first = 8*page 
    last = (page+1)*8
    if len(subjects)<last:
        last = len(subjects)
        btnmore = 0
    if first >= len(subjects):
        subjects=[]
    else:
        subjects=subjects[first:last]
    
    s = '''<div class="col-xl-4 col-lg-6 col-md-6">
					<div class="box_grid wow">
						<figure class="block-reveal">
							<div class="block-horizzontal"></div>
							
							<a href="/course/coursecreate"><img src="/static/homepage/img/add.png" class="img-fluid" alt=""></a>
							
							<div class="preview"><span>Thêm Khóa Học</span></div>
						</figure>
						<div class="wrapper" style="width:325px;height:175px">
                         <small> </small>
                         <br><br>
                            <h3 style="text-align:center;">Thêm những khóa học thú vị</h3>
                            <p></p>
							<div class="rating">
							<small></small></div>
                        </div>
                        <ul> 
							<li></li>
							<li></li>
							<li></li>
						</ul>
					</div>
				</div>'''
    if len(subjects) > 0:
        
        for sub in subjects:
            if sub.isenable == 1:
                condition = '''<div class="price">Công Khai</div>'''
            else:
                condition = '''<div class="price">Chưa Công Khai</div>'''
            
            rateSub = getrateSubject(sub)
            sublike = getlikeSubjectId(sub)
            star = ''
            for i in range(0,5):
                if i < rateSub[0]:
                    star += '''<i class="icon_star voted"></i>'''
                else:
                    star += '''<i class="icon_star"></i>'''

            linkover = '''/course/courseoverview/''' + str(sub.subjectid)
            linkdetail = '''/coursedetail/''' + str(sub.subjectid)
            linkchap = '''/course/''' + str(sub.subjectid) + '''/chapincourse'''

            temp = '''<div class="col-xl-4 col-lg-6 col-md-6">
                        <div class="box_grid wow">
                            <figure class="block-reveal">
                                <div class="block-horizzontal"></div>
                                <a href="'''  + linkchap + '''" class="wish_bt" ></a>
                                <a href="''' + linkdetail + '''"><img src="'''+ sub.avatar + '''" style="width:800px;height:194px;" class="img-fluid" alt=""></a>''' + condition + '''
                                <div class="preview"><span>Preview course</span></div>
                            </figure>
                            <div class="wrapper">
                                <small>''' + sub.enviromentcateid.enviromentcatename + ''''</small>
                                <h3>''' + sub.subjectname + '''</h3>
                                <p>''' + sub.description + '''</p>
                                <div class="rating">'''  + star +  '''
                                            
                                <small>''' + str(rateSub[1]) + '''</small></div>
                            </div>
                            <ul>
                                <li><i class="icon_clock_alt"></i>''' + str(rateSub[2]) + '''</li>
                                <li><i class="icon_like"></i>&nbsp ''' + str(sublike) + '''</li>
                                
                                <li><a href="''' + linkover +'''">Chỉnh Sửa</a></li>
                                
                            </ul>
                        </div>
                    </div>'''

            s += temp
        




        data = {
            's': s,
            'btnmore':btnmore
        }
    else:
        data = {
            's': s,
            'btnmore': btnmore
        }
    return JsonResponse(data)

def ajaxmanageteachpermit(request):
    subname = request.GET.get('subname', None)
    teachname = request.GET.get('teachname', None)

    subject = Subject.objects.filter(subjectname = subname)
    teach = teachname.split(" ")
    num = len(teach) - 1
    account = Account.objects.filter(username = teach[num])
    

    if (len(subject) != 0 and len(account) != 0):
        # nếu da cap rồi => k cho nua pass
        check = SubjectTeacher.objects.filter(accountid = account[0]).filter(subjectid=subject[0])
        if len(check) == 0:
            subteachnew = SubjectTeacher(
                accountid = account[0],
                subjectid = subject[0],
                createdate = datetime.now(),
                editdate = datetime.now(),
                isenable = 1, 
                note = '',
            )
            subteachnew.save()

    subjectteaches = SubjectTeacher.objects.filter(subjectid = subject[0]).order_by("-createdate")
    
    accusers = []
    for subteach in subjectteaches:
        acc = subteach.accountid
        userdetail = UserDetail.objects.get(accountid = acc)
        temp = AccountUserdetail(acc, userdetail)
        accusers.append(temp)


    s = ''
    for teach in accusers:
        # link = '''userprofile/''' + str(teach.account.accountid) + '''/'''
        temp = '''<div class="col-lg-4 col-md-6">
						<a class="box_feat" href="#">
							<i ><img style="width: 100px;height: 100px;border-radius: 50%" src="''' + teach.account.avatar + '''"></i>
							<br><br>
							<h5> ''' + teach.userdetail.lastname + ' ' + teach.userdetail.firstname + '''<br>
								<small>Giảng Viên Phụ</small>
							</h5>
							<button onclick="openpop(''' + str(teach.account.accountid) + ''')" class="btn_1" style="background-color: #ffc207"> Chặn Quyền</button>
						</a>
					</div>'''
        s += temp


    data = {
        's': s
    }
    return JsonResponse(data)


def ajaxdelteach(request):
    idacc = request.GET.get('idacc', None)
    namesub = request.GET.get('subname', None)
    
    account = Account.objects.get(accountid = idacc)

    subject = Subject.objects.get(subjectname = namesub)

    teacher = SubjectTeacher.objects.filter(subjectid=subject).filter(accountid = account)
    if len(teacher) > 0: 
        teacher[0].delete()

    subjectteaches = SubjectTeacher.objects.filter(subjectid = subject).order_by("-createdate")
    
    accusers = []
    for subteach in subjectteaches:
        acc = subteach.accountid
        userdetail = UserDetail.objects.get(accountid = acc)
        temp = AccountUserdetail(acc, userdetail)
        accusers.append(temp)


    s = ''
    for teach in accusers:
        # link = '''userprofile/''' + str(teach.account.accountid) + '''/'''
        temp = '''<div class="col-lg-4 col-md-6">
						<a class="box_feat" href="#">
							<i ><img style="width: 100px;height: 100px;border-radius: 50%" src="''' + teach.account.avatar + '''"></i>
							<br><br>
							<h5> ''' + teach.userdetail.lastname + ' ' + teach.userdetail.firstname + '''<br>
								<small>Giảng Viên Phụ</small>
							</h5>
							<button onclick="openpop(''' + str(teach.account.accountid) + ''')" class="btn_1" style="background-color: #ffc207"> Chặn Quyền</button>
						</a>
					</div>'''
        s += temp


    data = {
        's': s
    }
    return JsonResponse(data)





def ajaxdomteach(request):
    subname = request.GET.get('subname', None)
    subject = Subject.objects.filter(subjectname = subname)
    
    s = ''
    if len(subject) > 0:
        subjectteaches = SubjectTeacher.objects.filter(subjectid = subject[0]).order_by("-createdate")
        
        accusers = []
        for subteach in subjectteaches:
            acc = subteach.accountid
            userdetail = UserDetail.objects.get(accountid = acc)
            temp = AccountUserdetail(acc, userdetail)
            accusers.append(temp)


        
        for teach in accusers:
            # link = '''userprofile/''' + str(teach.account.accountid) + '''/'''
            temp = '''<div class="col-lg-4 col-md-6">
						<a class="box_feat" href="#">
                                <i ><img style="width: 100px;height: 100px;border-radius: 50%" src="''' + teach.account.avatar + '''"></i>
                                <br><br>
                                <h5> ''' + teach.userdetail.lastname + ' ' + teach.userdetail.firstname + '''<br>
                                    <small>Giảng Viên Phụ</small>
                                </h5>
                                <button onclick="openpop(''' + str(teach.account.accountid) + ''')" class="btn_1" style="background-color: #ffc207"> Chặn Quyền</button>
                            </a>
                        </div>'''
            s += temp


    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxsearchsub(request):
    account=Account.objects.get(username=request.session['username'])
    subname = request.GET.get('subname', None)
    subject= Subject.objects.filter(subjectname=subname)
    if len(subject)>0:
        flag=boolcheckTeacherPermit(account,subject[0])
    else:
        flag=True
    button = 1
    if flag :
        if  len(subject)>0:
            s='''<option value="0" selected="selected" >Chọn hoạt động </option>'''
            chapters = Chapter.objects.filter(subjectid=subject[0]) 
            archap=[]
            for chapter in chapters:
                archap.append(chapter.chapterid)
            lesssons=Lesson.objects.filter(chapterid__in=archap)
            arract=[]
            for lesson in lesssons:
                temps=getActivitySUBInLesson(lesson)
                for temp in temps:
                    arract.append(temp)
            print(len(arract))
            for act in arract:
                temp='''<option value="''' + str(act.activityid) +'''"  >'''+ act.activityname  +''' </option>'''
                s+=temp   
            button = 1
        else:
            s='''<option value="0" selected="selected" > Không có hoạt động nộp bài nào </option>'''
            button = 0
    else:
        s='''<option value="0" selected="selected" >Môn Học Của Bạn Không Tồn Tại </option>'''
        button = 1
    
    data={
        's':s,
        'button':button
    }
    return JsonResponse(data)

def ajaxsearchusersub(request):
    actid = int(request.GET.get('acid',None))
    s=''
  
    if actid > 0 :
        activity = Activity.objects.get(activityid=actid)
        activitysumittions = ActivitySubmittion.objects.filter(activityid=activity).order_by("-createdate")
        for activitysumittion in activitysumittions:
            print(activitysumittion.note)
            if activitysumittion.note == None or activitysumittion.note=="":
                link="/course/reviewsubmition/"+str(activitysumittion.activitysubmittionid)
                temp ='''	<div class="col-lg-4 col-md-6">
					<a class="box_feat" href="'''+ link +'''"  target="_blank">
						<i><img style="width: 100px;height: 100px;border-radius: 50%" src="'''+ activitysumittion.accountid.avatar +'''"></i>
						<br><h3>''' + activitysumittion.description +'''</h3>
						<br><h6>Chưa Đánh Giá</h6>
					</a>
					</div>  '''
                s+=temp
            else:
                link="/course/reviewsubmition/"+str(activitysumittion.activitysubmittionid)
                temp ='''	<div class="col-lg-4 col-md-6">
					<a class="box_feat" href="'''+ link +'''"  target="_blank">
						<i><img style="width: 100px;height: 100px;border-radius: 50%" src="'''+ activitysumittion.accountid.avatar +'''"></i>
						<br><h3 style="font-family: Arial;">''' + activitysumittion.description +'''</h3>
						<br><h6 style="font-family: Arial;">'''+ str(activitysumittion.note) +'''...</h6>
					</a>
					</div>  '''
                s+=temp
        if len(activitysumittions) == 0:
             s='<h3 style="font-family: Arial;">Chưa có bài nộp nào</h3>'
    else:
        s='<h3 style="font-family: Arial;">Hoạt động không tồn tại</h3>'
    data={
        's':s
    }
    return JsonResponse(data)


def ajaxgetpoint(request):
    account=Account.objects.get(username=request.session['username'])
    username=UserDetail.objects.get(accountid=account)
    point = request.GET.get('point', None)
    cmt = request.GET.get('cmt', None)
    idsubmit = request.GET.get('idsubmit', None)

    if (point.isdigit()):
        point = int(point)
    actsubmit = ActivitySubmittion.objects.get(activitysubmittionid=idsubmit)
    
    actsubmit.note = '<strong>Điểm: </strong> '+str(point) + '<br> <strong> Nhận Xét: </strong> ' + cmt+'<br><strong>Bởi giảng viên: </strong>'+username.lastname +" "+ username.firstname
    actsubmit.save()
    s=actsubmit.note
    data ={
        's':s
    }
    return JsonResponse(data)

        

def ajaxlookbf(request):
    request.session['look'] = '1'
    data = {

    }
    return JsonResponse(data)

def ajaxdellookbf(request):
    if request.session.has_key('look'):
        del request.session['look']
    data = {

    }
    return JsonResponse(data)
