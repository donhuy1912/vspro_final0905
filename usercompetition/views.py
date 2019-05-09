from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myfunction import *
from homepage.myclass import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator

# Create your views here.
def competition(request):
    nowtime=datetime.now()
    if request.session.has_key('username'):
        competitions = Competition.objects.filter(opendate__lte=nowtime).order_by('-createdate')
        account = Account.objects.get(username=request.session['username'])
        islog = 1
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            sumcomsubmitlike = 0
            if len(comsubmits) > 0:
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumcomsubmitlike += len(comsublikes)
                
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)

        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'account':account,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)
    else:
        competitions = Competition.objects.all().order_by('-createdate')
        islog = 0
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            sumcomsubmitlike = 0
            if len(comsubmits) > 0:
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumcomsubmitlike += len(comsublikes)
                
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)

        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)

def competitionpopular(request):
    if request.session.has_key('username'):
        competitions = Competition.objects.all()
        account = Account.objects.get(username=request.session['username'])
        islog = 1
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumcomsubmitlike += len(comsublikes)
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)

        if (len(listcompetition) > 0):
            # listcompetition = sorted(listcompetition, key = takeSeccond, reverse = True)
            listcompetition = sorted(listcompetition, key=operator.attrgetter('person'), reverse = True)

        # checked
        popular = 1   
            
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'account':account,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)
    else:
        competitions = Competition.objects.all()
        islog = 0
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumcomsubmitlike += len(comsublikes)
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)

        if (len(listcompetition) > 0):
            # listcompetition = sorted(listcompetition, key = takeSeccond, reverse = True)
            listcompetition = sorted(listcompetition, key=operator.attrgetter('person'), reverse = True)

        # checked
        popular = 1   
            
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)

def competitionenvironment(request, idenvir):
    if request.session.has_key('username'):
        competitions = Competition.objects.filter(enviromentcateid=idenvir).order_by('-createdate')
        account = Account.objects.get(username=request.session['username'])
        islog = 1
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1)
                    sumcomsubmitlike += len(comsublikes)
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)

        numpage = len(listcompetition)
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0
        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'account':account,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage': numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)
    else:
        competitions = Competition.objects.filter(enviromentcateid=idenvir).order_by('-createdate')
       
        islog = 0
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1)
                    sumcomsubmitlike += len(comsublikes)
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)

        numpage = len(listcompetition)
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0
        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog': islog,
            'listcompetition':listcompetition,
            'popular':popular,
            'environmentcates':environmentcates,
            'numpage': numpage,
        }
        
        return render(request, 'usercompetition/competition.html', context)

def competitionbylikeup(request, number):
    number = int(number)
    if request.session.has_key('username'):
        competitions = Competition.objects.all()
        account = Account.objects.get(username=request.session['username'])
        islog = 1
        
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumsubmitlike += len(comsublikes)
                if sumsubmitlike >= number:
                    temp = ClassCompetition(competition, sumsubmitlike, len(comsubmits))
                    listcompetition.append(temp)

        numpage = len(listcompetition)            
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'account':account,
            'listcompetition':listcompetition,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        return render(request, 'usercompetition/competition.html', context)
    else:
        competitions = Competition.objects.all()
        islog = 0
        
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumsubmitlike += len(comsublikes)
                if sumsubmitlike >= number:
                    temp = ClassCompetition(competition, sumsubmitlike, len(comsubmits))
                    listcompetition.append(temp)

        numpage = len(listcompetition)            
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog':islog,
            'listcompetition':listcompetition,
            'environmentcates':environmentcates,
            'numpage':numpage,
        }
        return render(request, 'usercompetition/competition.html', context)

def competitionbylikeunder100(request):
    if request.session.has_key('username'):
        competitions = Competition.objects.all()
        account = Account.objects.get(username=request.session['username'])
        islog = 1
        
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1)
                    sumcomsubmitlike += len(comsublikes)
                if len(comsublikes) < 100:
                    temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)    
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()
        
        context = {
            'islog':islog,
            'account':account,
            'listcompetition':listcompetition,
            'environmentcates':environmentcates,
            'numpage': numpage,
        }
        return render(request, 'usercompetition/competition.html', context)
    else:
        competitions = Competition.objects.all()
       
        islog = 0
        
        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            if len(comsubmits) > 0:
                sumcomsubmitlike = 0
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1)
                    sumcomsubmitlike += len(comsublikes)
                if len(comsublikes) < 100:
                    temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
        
        numpage = len(listcompetition)    
        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)
        
        # popular
        popular = 0

        # environment
        environmentcates = EnviromentCate.objects.all()
        
        context = {
            'islog':islog,
            'listcompetition':listcompetition,
            'environmentcates':environmentcates,
            'numpage': numpage,
        }
        return render(request, 'usercompetition/competition.html', context)

def competitiondetail(request, idcom):
    if request.session.has_key('username'):
        competition = Competition.objects.get(competitionid = idcom)
        competition.viewcount += 1
        competition.save()
        
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition).order_by('-createdate')

        account = Account.objects.get(username=request.session['username'])
        islog = 1
        
        checktime=0
        if competition.enddate< datetime.now():
            checktime=1
        if competition.opendate > datetime.now():
            checktime=2


        # Bài nộp gần đây
        numsubmit = len(comsubmits)
        if numsubmit >= 5:
            loadcomsubmit = comsubmits[0:5]
        else:
            loadcomsubmit = comsubmits[0:numsubmit]
        
        # Bài viết liên quan
        competitionbyenvirs = Competition.objects.filter(enviromentcateid = competition.enviromentcateid).exclude(competitionid=competition.competitionid).order_by('-createdate')
        numenvir = len(competitionbyenvirs)
        if  numenvir >= 10:
            competitionbyenvirs = competitionbyenvirs[0:10]
        else:
            competitionbyenvirs = competitionbyenvirs[0:numenvir]

        # Load rank
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
        listrank = []
        if len(comsubmits) > 0:
            for comsubmit in comsubmits:
                comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1) 
                temp = RankCompetition(comsubmit, len(comsublikes))
                listrank.append(temp)

        listresult = []
        if (len(listrank) > 0):
            listrank = sorted(listrank, key=operator.attrgetter('comsublike'), reverse = True)
            # Gán order
            rankorder = 0
            for rank in listrank:
                temp = RankName(rank, rankorder + 1)
                rankorder += 1
                listresult.append(temp)
        # Nếu listrank lớn 3
        
        if len(listresult) >= 3:
            listresult = listresult[0:3]
        else:
            listresult = listresult[0:len(listresult)]

        # bảng rank
        userrank = UserRank.objects.filter(enviromentcateid = competition.enviromentcateid)



        context = {
            'islog':islog,
            'account':account,
            'competition':competition,
            'numsubmit': numsubmit,
            'loadcomsubmit':loadcomsubmit,
            'competitionbyenvirs':competitionbyenvirs,
            'listresult':listresult,
            'userrank':userrank,
	    'checktime':checktime,
        }
        
        return render(request, 'usercompetition/competitiondetail.html', context)
    else:
        competition = Competition.objects.get(competitionid = idcom)
        islog = 0
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition).order_by('-createdate')
    
        checktime=0
        if competition.enddate< datetime.now():
            checktime=1
        if competition.opendate > datetime.now():
            checktime=2	
    
        # Bài nộp gần đây
        numsubmit = len(comsubmits)
        if numsubmit >= 5:
            loadcomsubmit = comsubmits[0:5]
        else:
            loadcomsubmit = comsubmits[0:numsubmit]
       
        # Bài viết liên quan
        competitionbyenvirs = Competition.objects.filter(enviromentcateid = competition.enviromentcateid).order_by('-createdate')
        numenvir = len(competitionbyenvirs)
        if  numenvir >= 10:
            competitionbyenvirs = competitionbyenvirs[0:10]
        else:
            competitionbyenvirs = competitionbyenvirs[0:numenvir]

        # Load rank
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
        listrank = []
        if len(comsubmits) > 0:
            for comsubmit in comsubmits:
                comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1) 
                temp = RankCompetition(comsubmit, len(comsublikes))
                listrank.append(temp)

        listresult = []
        if (len(listrank) > 0):
            listrank = sorted(listrank, key=operator.attrgetter('comsublike'), reverse = True)
            # Gán order
            rankorder = 0
            for rank in listrank:
                temp = RankName(rank, rankorder + 1)
                rankorder += 1
                listresult.append(temp)
        # Nếu listrank lớn 3
        
        if len(listresult) >= 3:
            listresult = listresult[0:3]
        else:
            listresult = listresult[0:len(listresult)]

        # bảng rank
        userrank = UserRank.objects.filter(enviromentcateid = competition.enviromentcateid)

        context = {
            'islog':islog,
            'competition':competition,
            'numsubmit':numsubmit,
            'loadcomsubmit':loadcomsubmit,
            'competitionbyenvirs':competitionbyenvirs,
            'listresult':listresult,
            'userrank':userrank,
	    'checktime':checktime,
        }
        return render(request, 'usercompetition/competitiondetail.html', context)

def competitionlistrank(request, idcom):
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        competition = Competition.objects.get(competitionid = idcom)
        
        # Load rank
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
        listrank = []
        if len(comsubmits) > 0:
            for comsubmit in comsubmits:
                comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1) 
                temp = RankCompetition(comsubmit, len(comsublikes))
                listrank.append(temp)

        listresult = []
        if (len(listrank) > 0):
            listrank = sorted(listrank, key=operator.attrgetter('comsublike'), reverse = True)
            # Gán order
            rankorder = 0
            for rank in listrank:
                temp = RankName(rank, rankorder + 1)
                rankorder += 1
                listresult.append(temp)
        
        numpage = len(listresult)
       
        # Page
        paginator = Paginator(listresult, 10) 
        page = request.GET.get('page')
        listresult = paginator.get_page(page)
       
        # bảng rank
        userrank = UserRank.objects.filter(enviromentcateid = competition.enviromentcateid)
        userrank5 = userrank[4]
        
        context = {
            'account':account,
            'islog':islog,
            'listresult':listresult,
            'userrank': userrank,
            'numpage':numpage,
            'userrank5':userrank5,
        }
        return render(request, 'usercompetition/competitionlistrank.html', context)
    else:
        islog = 0
        competition = Competition.objects.get(competitionid = idcom)
        
        # Load rank
        comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
        listrank = []
        if len(comsubmits) > 0:
            for comsubmit in comsubmits:
                comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status=1) 
                temp = RankCompetition(comsubmit, len(comsublikes))
                listrank.append(temp)

        listresult = []
        if (len(listrank) > 0):
            listrank = sorted(listrank, key=operator.attrgetter('comsublike'), reverse = True)
            # Gán order
            rankorder = 0
            for rank in listrank:
                temp = RankName(rank, rankorder + 1)
                rankorder += 1
                listresult.append(temp)
        
        numpage = len(listresult)
       
        # Page
        paginator = Paginator(listresult, 10) 
        page = request.GET.get('page')
        listresult = paginator.get_page(page)
       
        # bảng rank
        userrank = UserRank.objects.filter(enviromentcateid = competition.enviromentcateid)
        userrank5 = userrank[4]
        
        context = {
            'islog':islog,
            'listresult':listresult,
            'userrank': userrank,
            'numpage':numpage,
            'userrank5':userrank5,
        }
        return render(request, 'usercompetition/competitionlistrank.html', context)

def competitionsubmitiondetail(request, idsubmit):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        comsubmit = CompetitionSubmittion.objects.get(competitionsubmittionid = idsubmit)
        
        checklike = CompetitionSubmittionLike.objects.filter(competitionsubmittionid = comsubmit).filter(accountid = account)
        liked = 0
        if len(checklike) > 0:
            liked = 1
        
        islog = 1
        # comment
        comments = CompetitionSubmittionReply.objects.filter(competitionsubmittionid = comsubmit).order_by('-createdate')

        # Like
        numlike = CompetitionSubmittionLike.objects.filter(competitionsubmittionid = comsubmit)
        
        context = {
            'islog': islog,
            'account': account,
            'comsubmit': comsubmit,
            'liked': liked,
            'checklike': checklike,
            'numcomment': len(comments),
            'comments': comments,
            'numlike': len(numlike),
        }
        
        return render(request, 'usercompetition/competitionsubmitiondetail.html', context)
    else:
        comsubmit = CompetitionSubmittion.objects.get(competitionsubmittionid = idsubmit)
        islog = 0
        # comment
        comments = CompetitionSubmittionReply.objects.filter(competitionsubmittionid = comsubmit).order_by('-createdate')

        # Like
        numlike = CompetitionSubmittionLike.objects.filter(competitionsubmittionid = comsubmit)
        
        context = {
            'islog': islog,
            'comsubmit': comsubmit,
            'numcomment': len(comments),
            'comments': comments,
            'numlike': len(numlike),
        }   
        
        return render(request, 'usercompetition/competitionsubmitiondetail.html', context)

def competitioncreate(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2):
            environmentcates = EnviromentCate.objects.all()

            if request.method == "POST":
                enviromentcateid = request.POST.get('enviromentcateid')
                comname = request.POST.get('subjectname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                datebegin = request.POST.get('datebegin')
                dateend = request.POST.get('dateend')
                try:
                    imgCom = request.FILES.get('avatar')
                except:
                    imgCom = None
                note = request.POST.get('note')

                # xu ly 
                if imgCom != None:
                    imgComURL = tokenFile(imgCom)
                else:
                    imgComURL = ''

                competitionNew = Competition(
                    accountid = account,
                    enviromentcateid = EnviromentCate.objects.get(enviromentcateid = enviromentcateid),
                    competitionname = comname,
                    description = description,
                    content = content,
                    avatar = imgComURL,
                    createdate = datetime.now(),
                    editdate = datetime.now(),
                    opendate = datebegin,
                    enddate = dateend,
                    viewcount = 0,
                    likecount = 0,
                    isenable = 0,
                    note = note,
                )
                competitionNew.save()
                
                return redirect('usercompetition:listcompetition')

            
            context = {
                'account':account,
                'environmentcates':environmentcates,
            }
            return render(request, 'usercompetition/competitioncreate.html', context)
        
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def listcompetition(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2):
            competitions = Competition.objects.filter(accountid = account).order_by('-createdate')

            listcompetition = []
            for competition in competitions:
                comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
                sumcomsubmitlike = 0
                if len(comsubmits) > 0:
                    for comsubmit in comsubmits:
                        comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                        sumcomsubmitlike += len(comsublikes)
                    
                    temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
                else:
                    temp = ClassCompetition(competition, 0, 0)
                listcompetition.append(temp)
            
            numpage = len(listcompetition)

            # Page
            paginator = Paginator(listcompetition, 2) 
            page = request.GET.get('page')
            listcompetition = paginator.get_page(page)

            
            context = {
                'account':account,
                'listcompetition':listcompetition,
                'numpage':numpage,
            }
            return render(request, 'usercompetition/competitionlist.html', context)
        
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def listcompetition2(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        
        competitions = Competition.objects.all().exclude(enviromentcateid__lt=4).order_by('-createdate')

        listcompetition = []
        for competition in competitions:
            comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition)
            sumcomsubmitlike = 0
            if len(comsubmits) > 0:
                for comsubmit in comsubmits:
                    comsublikes = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=comsubmit).filter(status = 1)
                    sumcomsubmitlike += len(comsublikes)
                    
                temp = ClassCompetition(competition, sumcomsubmitlike, len(comsubmits))
            else:
                temp = ClassCompetition(competition, 0, 0)
            listcompetition.append(temp)
            
        numpage = len(listcompetition)

        # Page
        paginator = Paginator(listcompetition, 2) 
        page = request.GET.get('page')
        listcompetition = paginator.get_page(page)

            
        context = {
                'account':account,
                'listcompetition':listcompetition,
                'numpage':numpage,
            }
        return render(request, 'usercompetition/competitionlist2.html', context)
        
    else:
        return redirect('homepage:index')


def competitionedit(request, idcom):
    if request.session.has_key('username'):
        account = Account.objects.get(username=request.session['username'])
        competition = Competition.objects.get(competitionid = idcom)
        if (account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2) and competition.accountid == account:
            environmentcates = EnviromentCate.objects.all()
            competition.enddate=competition.enddate.date().strftime("%Y-%m-%d")
            competition.opendate=competition.opendate.date().strftime("%Y-%m-%d")
            competition.avatar =competition.avatar.replace("/media/","")
            if request.method == "POST":
                enviromentcateid = request.POST.get('enviromentcateid')
                comname = request.POST.get('subjectname')
                description = request.POST.get('description')
                content = request.POST.get('content')
                datebegin = request.POST.get('datebegin')
                dateend = request.POST.get('dateend')
                try:
                    imgCom = request.FILES.get('avatar')
                except:
                    imgCom = None
                
                note = request.POST.get('note')

                # xu ly 
                if imgCom != None:
                    imgComURL = tokenFile(imgCom)
                else:
                    imgComURL = '/media/' + competition.avatar

                competition.enviromentcateid = EnviromentCate.objects.get(enviromentcateid = enviromentcateid)
                competition.competitionname = comname
                competition.description = description
                competition.content = content
                competition.avatar = imgComURL
                competition.editdate = datetime.now()
                competition.opendate = datebegin
                competition.enddate = dateend
                competition.note = note
                
                competition.save()
                
                return redirect('usercompetition:listcompetition')

            
            context = {
                'account':account,
                'environmentcates':environmentcates,
                'competition': competition,
            }
            return render(request, 'usercompetition/competitionedit.html', context)
        
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
