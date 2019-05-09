from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import *
from homepage.myfunction import *
from django.core.mail import send_mail
from homepage.myclass import *
from django.http import JsonResponse
from operator import itemgetter, attrgetter
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# --- Hàm index --- #
def index(request):
     # Lấy 4 tin tức mới nhất (theo createdate)
    newss = News.objects.all().order_by('-createdate')[0:5]
    newsuserdetaillist = []
    for news in newss:
        userdetail = UserDetail.objects.filter(accountid = news.accountid)
        temp = NewsUserdetail(news, userdetail)
        newsuserdetaillist.append(temp)

    # Lấy 5 môn lên, sắp xếp theo tính phổ biến(số lượng đăng kí)
    listSubjectid = top5subjects()
    subjects = []
    for i in range(len(listSubjectid)):
        subjectByid = Subject.objects.get(subjectid = listSubjectid[i])
        subjects.append(subjectByid)
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
    count = len(EnviromentCate.objects.all())
    
    # Cuộc thi
    competitions = Competition.objects.all().order_by('-viewcount')
    if len(competitions) > 6:
        competitions = competitions[0:6]
    
    # Projectshare: Dự án
    projectshares = ProjectShare.objects.all().order_by('-viewcount')
    if len(projectshares) > 6:
        projectshares = projectshares[0:6]

    # Thành viên tích cực
    arrMember = []
    accounts = Account.objects.all()
    for account in accounts:
        userdetail = UserDetail.objects.get(accountid = account)
        enrolls = Enrollment.objects.filter(accountid = account)
        numenroll = len(enrolls)
        if numenroll != 0:
            num = 0
            for enroll in enrolls:
                numrep_eachacc = ActivityReply.objects.filter(enrollmentid = enroll)
                num += len(numrep_eachacc)
            temp = UserDetailActivityRep(account, userdetail.firstname, num, numenroll)
            arrMember.append(temp)    
    
    if len(arrMember) > 0:
        arrMember = sorted(arrMember, key=operator.attrgetter('numrep'), reverse = True)

    if len(arrMember) > 3:
        arrMember = arrMember[0:3]

    hours = datetime.now().hour
    mins = datetime.now().minute
    hm = str(hours) + ":" + str(mins)
    # Tìm xem có session hay không. Nếu có gán islog = 1, username = tên session
    islog = 0
    user_log = request.session.has_key('username')
    if user_log:
        islog = 1
        username = request.session['username']
        account =  Account.objects.get(username = username)
        context = {
            'username':username,
            'islog': islog,
            'account':account,
            'arrSubMas':arrSubMas,
            'count':count,
            'competitions': competitions,
            'projectshares':projectshares,
            'arrMember': arrMember,
            'newss': newss,
            'newsuserdetaillist': newsuserdetaillist,
            'hm':hm,
        }
    else:
        context = {
            'islog': islog,
            'subjects':subjects,
            'arrTup': arrTup,
            'arrSubMas':arrSubMas,
            'count':count,
            'competitions': competitions,
            'projectshares': projectshares,
            'arrMember':arrMember,
            'newss': newss,
            'newsuserdetaillist': newsuserdetaillist,
            'hm':hm,
    }
    
    return render(request, 'homepage/index.html', context)

# Tìm kiếm theo tên khóa học
def searchsub(request, subname):
    
    if subname == '':
        return redirect('homepage:index')
    searchsubjects = Subject.objects.filter(subjectname__icontains=subname)
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
            
            
        paginator = Paginator(arrSubM, 6) 
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
            
        paginator = Paginator(arrSubM, 6) 
        page = request.GET.get('page')
        arrSubM = paginator.get_page(page)

        context={
                'arrSubM':arrSubM,
                'show':show,
                'islog':islog,
            }
        return render(request, 'homepage/listsubject.html', context)
        

def resource(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context = {
            'account': account,
            'islog': islog,
        }
        return render(request, 'homepage/resource.html', context)
    context = {
        'islog': islog,
    }
    return render(request, 'homepage/resource.html', context)

# --- Hàm Login --- # 
def myLogin(request):
    # Kiểm tra có sessions chưa
    if request.session.has_key('username'):
        return redirect('homepage:index')
    else:
        if request.method == "POST":
            username = request.POST.get('user')
            password = request.POST.get('pass')
            # Kiểm tra tài khoản tồn tại hay không
            flaglogin = boolcheckAccount(username, password)
            if flaglogin:
                account = Account.objects.get(username=username)
                # Kiểm tra tài khoản isEnable chưa
                if account.isenable == 1:
                    # Đăng nhập
                    request.session['username'] = account.username
                    return redirect('homepage:index')
                elif account.isenable == 0:
                    return redirect('homepage:activeaccount')
            else:
                # Báo lỗi khi tài khoản không chính xác
                messages.error(request, 'Tài khoản và mật khẩu không chính xác')
                return redirect('homepage:login')
    
    return render(request, 'homepage/login.html')

# --- Hàm Logout --- #
def myLogout(request):
    try:
        del request.session['username']
        del request.session['look']
    except:
        pass
    return redirect('homepage:index')

# --- Hàm đăng kí account --- #
def myRegister(request):
    # Kiểm tra
        #1 Kiểm tra đầy đủ các thông tin yêu cầu
        #2 Kiểm tra dữ liệu hợp lệ (số điện thoại, email) 
        #3 Kiểm tra trùng tên đăng nhập
        #4 Kiểm tra password đúng với yêu cầu & password1 = password2
        #5 Kiểm tra có khoảng trắng trong username & password
        #6 Kiểm tra trùng email

    if request.method == "POST":
        username = request.POST.get('user')
        passwd1 = request.POST.get('pass1')
        passwd2 = request.POST.get('pass2')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if (username == '' or passwd1 =='' or passwd2 =='' or fname =='' or lname =='' or email ==''):
            messages.error(request, 'Vui lòng điền đầy đủ các thông tin dấu *')
            return redirect('homepage:register')
        elif (boolcheckSpace(username) or boolcheckSpace(passwd1)):
            messages.error(request, 'Không được có khoảng trắng trong tên đăng nhập hoặc mật khẩu')
            return redirect('homepage:register')
        elif boolcheckUser(username):
            messages.error(request, 'Tên đăng nhập đã tồn tại')
            return redirect('homepage:register')
        elif (not isEmail(email)):
            messages.error(request, 'Email không hợp lệ')
            return redirect('homepage:register')
        elif (not boolcheckphoneNumber(phone)):
            messages.error(request, 'Số điện thoại không hợp lệ')
            return redirect('homepage:register')
        elif not (boolcheckPassword(passwd1)):
            messages.error(request, 'Mật khẩu phải dài hơn 8 ký tự bao gồm chữ hoa, chữ thường và số')
            return redirect('homepage:register')
        elif (passwd1 != passwd2):
            messages.error(request, 'Mật khẩu không trùng khớp')
            return redirect('homepage:register')
        elif boolcheckEmail(email):
            messages.error(request, 'Email này đã được sử dụng cho tài khoản khác')
            return redirect('homepage:register')
        else:
            account = Account( 
                                accounttypeid = AccountType.objects.get(accounttypeid = 3),
                                username = username,
                                password = hashPassword(passwd1), 
                                createdate =  datetime.now(), 
                                editdate =  datetime.now(),
                                avatar = '/media/userava.png',
                                resetcode = '',
                                isenable = 0,  
            )
            account.save()
            userdetail = UserDetail( 
                                    accountid = Account.objects.get(username = request.POST.get('user')),
                                    firstname = fname, 
                                    lastname = lname, 
                                    birthday =  datetime.now(),
                                    address = ' ', 
                                    phonenumber = phone, 
                                    email = email, 
                                    isenable = 1,
            )
            userdetail.save()

            return redirect('homepage:login')

    return render(request, 'homepage/register.html')

# Hàm load trang Giới Thiệu
def introduction(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context={
            'account':account,
            'islog': islog,
        }
        
        return render(request, 'homepage/introduction.html', context)
    
    context={
            'islog': islog,
        }
    
    return render(request, 'homepage/introduction.html', context)

# Hàm load trang Tầm Nhìn
def vision(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context = {
            'account': account,
            'islog': islog,
        }
        return render(request, 'homepage/vision.html', context)
    context = {
        'islog': islog,
    }
    return render(request, 'homepage/vision.html', context)

# Hàm load trang Chuyên gia
def team(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context = {
            'account': account,
            'islog': islog,
        }
        return render(request, 'homepage/team.html', context)
    context = {
        'islog': islog,
    }
    return render(request, 'homepage/team.html', context)


# Hàm load trang Về Chúng Tôi
def aboutUs(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context = {
            'account': account,
            'islog': islog,
        }
        return render(request, 'homepage/aboutus.html', context)
    context = {
        'islog': islog,
    }
    return render(request, 'homepage/aboutus.html', context)
	
# My Profile
def myProfile(request, id):
    account = Account.objects.get(accountid = id)
    userdetail = UserDetail.objects.get(accountid = account.accountid)
    userdetail.birthday = userdetail.birthday.strftime("%d-%m-%Y")
    enrollments = Enrollment.objects.filter(accountid = account.accountid)
    subList = []
    notsubList = []
    subjects = []
    for enrollment in enrollments:
        subjects.append(enrollment.subjectid)
        if boolcheckSubjectProcess(enrollment.subjectid,account) == True:
            subList.append(enrollment.subjectid)
        else:
            notsubList.append(enrollment.subjectid)
    lensub = len(subList)
    lennotsub = len(notsubList)

    # load các cuộc thi mà người học đã tham gia nộp bài
    projectshares = ProjectShare.objects.filter(accountid = account.accountid).order_by('createdate')
    lenpro = len(projectshares)
    projectshares = projectshares[0:4]
    

    forums = Forum.objects.filter(accountid = account.accountid).order_by('createdate')
    lenfor = len(forums)
    forums = forums[0:5]

    forumreplys = ForumReply.objects.filter(accountid = account.accountid)
    lenforrep = len(forumreplys)

    projectsharereplys = ProjectShareReply.objects.filter(accountid = account.accountid)
    lenprorep = len(projectsharereplys)

    competitionsubmittions = CompetitionSubmittion.objects.filter(accountid = account.accountid)
    lencompsub = len(competitionsubmittions)

    context = {
        'account':account,
        'userdetail': userdetail,
        'subList': subList,
        'notsubList': notsubList,
        'lensub': lensub,
        'lennotsub': lennotsub,
        'competitionsubmittions': competitionsubmittions,
        'lencompsub': lencompsub,
        # 'competitions': competitions,
        'forumreplys':forumreplys,
        'lenforrep': lenforrep,
        'forums': forums,
        'lenfor': lenfor,
        'projectshares': projectshares,
        'lenpro': lenpro,
        'projectsharereplys':projectsharereplys,
        'lenprorep': lenprorep,
    }
    return render(request, 'homepage/myprofile.html', context)




def userprofile(request, idguest):
    account = Account.objects.get(accountid = idguest)
    userdetail = UserDetail.objects.get(accountid = account.accountid)
    islog = 0    
    userdetail.birthday = userdetail.birthday.strftime("%d-%m-%Y")
    enrollments = Enrollment.objects.filter(accountid = account.accountid)
    subList = []
    notsubList = []
    subjects = []
    for enrollment in enrollments:
        subjects.append(enrollment.subjectid)
        if boolcheckSubjectProcess(enrollment.subjectid,account) == True:
            subList.append(enrollment.subjectid)
        else:
            notsubList.append(enrollment.subjectid)
    lensub = len(subList)
    lennotsub = len(notsubList)

    # load các cuộc thi mà người học đã tham gia nộp bài
    projectshares = ProjectShare.objects.filter(accountid = account.accountid).order_by('createdate')
    lenpro = len(projectshares)
    projectshares = projectshares[0:4]
    

    forums = Forum.objects.filter(accountid = account.accountid).order_by('createdate')
    lenfor = len(forums)
    forums = forums[0:5]

    forumreplys = ForumReply.objects.filter(accountid = account.accountid)
    lenforrep = len(forumreplys)

    projectsharereplys = ProjectShareReply.objects.filter(accountid = account.accountid)
    lenprorep = len(projectsharereplys)

    competitionsubmittions = CompetitionSubmittion.objects.filter(accountid = account.accountid)
    lencompsub = len(competitionsubmittions)
    #####
    mycourses = Subject.objects.filter(accountid=account)
    
    subteaches=SubjectTeacher.objects.filter(accountid=account)
    arrSub = []
    for mycourse in mycourses:
        arrSub.append(mycourse)
    for sub in subteaches:
        arrSub.append(sub.subjectid)

    if len(arrSub) >10:
        arrSub = arrSub[0:10]
    stt=1
    for sub in arrSub:
        sub.note = stt
        stt += 1
    if request.session.has_key('username'):
        accounted = Account.objects.get(username = request.session['username'])
        
        islog = 1
        context = {
            'arrSub': arrSub,
            'islog': islog,
            'accounted': accounted,
            'account':account,
            'userdetail': userdetail,
            'subList': subList,
            'notsubList': notsubList,
            'lensub': lensub,
            'lennotsub': lennotsub,
            'competitionsubmittions': competitionsubmittions,
            'lencompsub': lencompsub,
            'forumreplys':forumreplys,
            'lenforrep': lenforrep,
            'forums': forums,
            'lenfor': lenfor,
            'projectshares': projectshares,
            'lenpro': lenpro,
            'projectsharereplys':projectsharereplys,
            'lenprorep': lenprorep,
        }
    else:
        context = {
            'arrSub': arrSub,
            'account':account,
            'islog': islog,         
            'userdetail': userdetail,
            'subList': subList,
            'notsubList': notsubList,
            'lensub': lensub,
            'lennotsub': lennotsub,
            'competitionsubmittions': competitionsubmittions,
            'lencompsub': lencompsub,
            'forumreplys':forumreplys,
            'lenforrep': lenforrep,
            'forums': forums,
            'lenfor': lenfor,
            'projectshares': projectshares,
            'lenpro': lenpro,
            'projectsharereplys':projectsharereplys,
            'lenprorep': lenprorep,
        }
    
    return render(request, 'homepage/userprofile.html', context)
# --- Hàm chỉnh sửa profile --- #
def editMyProfile(request, id):
    account = Account.objects.get(accountid = id)
    userdetail = UserDetail.objects.get(accountid = account.accountid)
    userdetail.birthday = userdetail.birthday.strftime("%Y-%m-%d")
    context = {
        'account':account,
        'userdetail': userdetail
    }
    if request.method == "POST":
        lname = request.POST.get('lastname')
        fname = request.POST.get('firstname')
        address = request.POST.get('address')
        phone = request.POST.get('phonenumber')
        email = request.POST.get('email')
        birthday  = request.POST.get('birthday')
       
        # Lấy avatar
        try:
            avatar = request.FILES['avatar']
        except:
            avatar = None
        if avatar != None:
            account.avatar = tokenFile(avatar) 
        
        # Lưu dữ liệu
        if boolcheckphoneNumber(phone):
            userdetail.phonenumber = phone
        else:
            messages.error(request, 'Số điện thoại không hợp lệ')
            return redirect('homepage:editmyprofile', id = account.accountid)
        if isEmail(email):
            userdetail.email = email
        else:
            messages.error(request, 'Email không hợp lệ')
            return redirect('homepage:editmyprofile', id = account.accountid)
        
        userdetail.birthday = birthday
        userdetail.lastname = lname
        userdetail.firstname = fname
        userdetail.address = address

        userdetail.save()
        account.save()

        return redirect('homepage:myprofile', id = account.accountid)

    return render(request, 'homepage/editmyprofile.html', context)

# --- Hàm changepassword --- #
def myChangepassword(request, id):
    account = Account.objects.get(accountid = id)
    if request.session.has_key('username'):
        if Account.objects.get(username = request.session['username']) == account:
            if request.method == "POST":
                oldpass  = request.POST.get('oldpass')
                newpass1 = request.POST.get('newpass1')
                newpass2 = request.POST.get('newpass2')

                if (oldpass == '' or newpass1 == '' or newpass2 == ''):
                    messages.error(request, 'Vui lòng điền đầy đủ thông tin yêu cầu')
                    return redirect('homepage:changepassword', id = account.accountid)
                elif not (boolcheckPassword(newpass1)):
                    messages.error(request, 'Mật khẩu phải dài hơn 8 ký tự bao gồm chữ hoa, chữ thường và số')
                    return redirect('homepage:changepassword', id = account.accountid)
                elif (newpass1 != newpass2):
                    messages.error(request, 'Mật khẩu không trùng khớp')
                    return redirect('homepage:changepassword', id = account.accountid)
                elif not (account.password == hashPassword(oldpass)):
                    messages.error(request, 'Mật khẩu không chính xác')
                    return redirect('homepage:changepassword', id = account.accountid)
                else:
                    account.password = hashPassword(newpass1) 
                    account.save()
                
                try:
                    del request.session['username']
                except:
                    pass
                
                return redirect('homepage:login')
        
            return render(request, 'homepage/changepassword.html', {'account':account}) 
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

    # return render(request, 'homepage/changepassword.html', {'account':account}) 

# --- Hàm forget password --- #

# Hàm trang forgotpassword
def passForgot(request):
    if request.method == "POST":
        username = request.POST.get('user')
        if boolcheckUser(username):
            # Khởi tạo random code
            rancode = randomcode()
            # Lấy email theo username
            account = Account.objects.get(username=username)
            userdetail = UserDetail.objects.get(accountid = account.accountid)
            # Gửi email cho người dùng
            send_mail('VS-Programming Learning',
                rancode,
                'vsprodhsp@gmail.com',
                [userdetail.email],
                fail_silently=False
            )
            account.resetcode = rancode
            account.save()
            # Tạo session theo tên & mã xác nhận
            request.session['tencode'] = username + ' ' + rancode
            # Chuyển sang trang confirmpassword
            return redirect('homepage:confirmpass')
        else:
            messages.error(request, 'Tên tài khoản không tồn tại')
            return redirect('homepage:forgotpass')

    return render(request, 'homepage/forgotpassword.html')

# Hàm trang confirmpassword
def passConfirm(request):
    if request.session.has_key('tencode'):
        username = getUsername(request.session['tencode'])    
        account = Account.objects.get(username = username)
        
        if request.method == "POST":
            code = request.POST.get('maxacnhan')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            del request.session['tencode']

            if (pass1 == '' or pass2 == '' or code == ''):
                messages.error(request, 'Vui lòng điền đầy đủ thông tin yêu cầu')
                return redirect('homepage:confirmpass')
            elif not boolcheckInt(code):
                messages.error(request, 'Mã xác nhận không chính xác')
                return redirect('homepage:confirmpass')
            elif (int(account.resetcode) != int(code)):
                messages.error(request, 'Mã xác nhận không chính xác')
                return redirect('homepage:confirmpass')
            elif not (boolcheckPassword(pass1)):
                messages.error(request, 'Mật khẩu phải dài hơn 8 ký tự bao gồm chữ hoa, chữ thường và số')
                return redirect('homepage:confirmpass')
            elif (pass1 != pass2):
                messages.error(request, 'Mật khẩu không trùng khớp')
                return redirect('homepage:confirmpass')
            else:
                account.password = hashPassword(pass1)
                account.save()
                return redirect('homepage:login')
    
    return render(request,'homepage/confirmpassword.html')

# --- Hàm active Account --- #

# Hàm nhập mã xác nhận active account
def activeAccount(request):
    if request.method == "POST":
        username = request.POST.get('user')
        if boolcheckUser(username):
            # Khởi tạo random code
            rancode = randomcode()
            # Lấy email theo username
            account = Account.objects.get(username=username)
            userdetail = UserDetail.objects.get(accountid = account.accountid)
            # Gửi email cho người dùng
            send_mail('VS-Programming Learning',
                rancode,
                'vsprodhsp@gmail.com',
                [userdetail.email],
                fail_silently=False
            )
            account.resetcode = rancode
            account.save()
            # Tạo session theo tên & mã xác nhận
            request.session['tencode'] = username + ' ' + rancode
            # Chuyển sang trang confirmaccount
            return redirect('homepage:confirmaccount')
        else:
            messages.error(request, 'Tên tài khoản không tồn tại')
            return redirect('homepage:activeaccount')

    return render(request, 'homepage/activeaccount.html')

# Hàm nhập mã xác nhận confirm account
def confirmAccount(request):
    if request.session.has_key('tencode'):
        username = getUsername(request.session['tencode'])    
        account = Account.objects.get(username = username)
        
        if request.method == "POST":
            code = request.POST.get('maxacnhan')
            del request.session['tencode']
        
            if (code == ''):
                messages.error(request, 'Vui lòng điền đầy đủ thông tin yêu cầu')
                return redirect('homepage:confirmaccount')
            elif not boolcheckInt(code):
                messages.error(request, 'Mã xác nhận không chính xác')
                return redirect('homepage:confirmaccount')
            elif (int(account.resetcode) != int(code)):
                messages.error(request, 'Mã xác nhận không chính xác')
                return redirect('homepage:confirmaccount')
            else:
                account.isenable = 1
                account.save()
                return redirect('homepage:login')
    
    return render(request,'homepage/confirmaccount.html')

#Hàm kiểm tra tên đăng nhập đã tồn tại chưa
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

#Hàm kiểm tra email đã tồn tại chưa
# def validate_email(request):
#     email = request.GET.get('email', None)
#     data = {
#         'is_taken': UserDetail.objects.filter(email__iexact=email).exists()
#     }
#     return JsonResponse(data)

def adminchat(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        userdetail=UserDetail.objects.get(accountid=account)
        context = {
                   'account':account,
                    'userdetail':userdetail
                        }
        return render(request,'homepage/inbox.html',context)
    else:
        return redirect('homepage:index')

def userguide(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context={
            'account':account,
            'islog': islog,
        }
        return render(request, 'homepage/userguide.html', context)
    
    context={
            'islog': islog,
        }
    
    return render(request, 'homepage/userguide.html', context)

def sitemap(request):
    islog = 0
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context={
            'account':account,
            'islog': islog,
        }
        return render(request, 'homepage/sitemap.html', context)
    
    context={
            'islog': islog,
        }
    
    return render(request, 'homepage/sitemap.html', context)

def contact(request):
    islog = 0
    # POST method
    if request.method == "POST":
        fname = request.POST.get('firstname') 
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        content = request.POST.get('content')
        fullname=lname+' '+fname+' Hỗ trợ'
        fullcontent=''' Bởi '''+email+''' 
        '''+ content
        send_mail(fullname,
                fullcontent,
                'vsprodhsp@gmail.com',
                ['vsprosuperuser@gmail.com'],
                fail_silently=False
            )
        return redirect('homepage:contact')

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        context={
            'account':account,
            'islog': islog,
        }
        
        return render(request, 'homepage/contact.html', context)
    
    context={
            'islog': islog,
        }
    
    return render(request, 'homepage/contact.html', context)
