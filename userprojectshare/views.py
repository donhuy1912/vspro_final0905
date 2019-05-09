from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myclass import *
from homepage.myfunction import tokenFile
import operator
from datetime import datetime

# Create your views here.
def projectshare(request):
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        
        allprojectshare = ProjectShare.objects.all()
        projectshares = allprojectshare.order_by('-viewcount')
        if len(projectshares) > 5:
            projectshares = projectshares[0:5]
        
        projectsharelast = allprojectshare.order_by('-createdate')
        if len(projectsharelast) > 9:
            projectsharelast = projectsharelast[0:9]
        
        
        # rank like
        arrProject = []
        for projectshare in allprojectshare:
            prolikes = ProjectShareLike.objects.filter(projectsharetopicid = projectshare)
            temp = ProShare(projectshare, len(prolikes))
            arrProject.append(temp)
        
        if (len(arrProject) > 0):
            listproshare = sorted(arrProject, key=operator.attrgetter('countlike'), reverse = True)
        else:
            listproshare = []

        if len(listproshare) > 6:
            listproshare = listproshare[0:6]

        context = {
            'islog': islog,
            'account': account,
            'projectshares': projectshares,
            'projectsharelast' : projectsharelast,
            'listproshare': listproshare,
        }
        return render(request, 'userprojectshare/projectshare.html', context)
    else:
        islog = 0
        allprojectshare = ProjectShare.objects.all()
        projectshares = allprojectshare.order_by('-viewcount')
        if len(projectshares) > 5:
            projectshares = projectshares[0:5]
        
        projectsharelast = allprojectshare.order_by('-createdate')
        if len(projectsharelast) > 9:
            projectsharelast = projectsharelast[0:9]
        
        # rank like
        arrProject = []
        for projectshare in allprojectshare:
            prolikes = ProjectShareLike.objects.filter(projectsharetopicid = projectshare)
            temp = ProShare(projectshare, len(prolikes))
            arrProject.append(temp)
        
        if (len(arrProject) > 0):
            listproshare = sorted(arrProject, key=operator.attrgetter('countlike'), reverse = True)

        if len(listproshare) > 6:
            listproshare = listproshare[0:6]

        context = {
            'islog': islog,
            'projectshares': projectshares,
            'projectsharelast' : projectsharelast,
            'listproshare': listproshare,
        }
        return render(request, 'userprojectshare/projectshare.html', context)

def projectsharenew(request):
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])

        projectsharenewall = ProjectShare.objects.all().order_by('-createdate')
        if len(projectsharenewall) > 9:
            projectsharenew = projectsharenewall[0:9]
        else:
            projectsharenew = projectsharenewall

        environmentcates = EnviromentCate.objects.all()
        

        context = {
            'islog': islog,
            'account': account,
            'projectsharenew': projectsharenew,
            'environmentcates': environmentcates,
        }
        return render(request, 'userprojectshare/projectsharenew.html', context)
    else:
        islog = 0

        projectsharenewall = ProjectShare.objects.all().order_by('-createdate')
        if len(projectsharenewall) > 9:
            projectsharenew = projectsharenewall[0:9]
        else:
            projectsharenew = projectsharenewall

        environmentcates = EnviromentCate.objects.all()


        context = {
            'islog': islog,
            'projectsharenew': projectsharenew,
            'environmentcates': environmentcates,
        }
        return render(request, 'userprojectshare/projectsharenew.html', context)

def projectsharelove(request):
    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])

        projectshareloveall = ProjectShare.objects.all().order_by('-viewcount')
        if len(projectshareloveall) > 9:
            projectsharelove = projectshareloveall[0:9]
        else:
            projectsharelove = projectshareloveall
        
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog': islog,
            'account': account,
            'projectsharelove': projectsharelove,
            'environmentcates': environmentcates,
        }
        return render(request, 'userprojectshare/projectsharelove.html', context)
    else:
        islog = 0

        projectshareloveall = ProjectShare.objects.all().order_by('-viewcount')
        if len(projectshareloveall) > 9:
            projectsharelove = projectshareloveall[0:9]
        else:
            projectsharelove = projectshareloveall
        
        environmentcates = EnviromentCate.objects.all()

        context = {
            'islog': islog,
            'projectsharelove': projectsharelove,
            'environmentcates': environmentcates,
        }
        return render(request, 'userprojectshare/projectsharelove.html', context)

def projectsharedetail(request, idpro):
    projectshare = ProjectShare.objects.get(projectsharetopicid = idpro)
    projectshare.viewcount += 1
    projectshare.save()

    if request.session.has_key('username'):
        islog = 1
        account = Account.objects.get(username = request.session['username'])
        

        # cmt & like
        prosharereps = ProjectShareReply.objects.filter(projectsharetopicid = projectshare).order_by('-createdate')
        if len(prosharereps) > 5:
            prosharereps = prosharereps[0:5]
        prosharelikes = ProjectShareLike.objects.filter(projectsharetopicid = projectshare)



        # dự án liên quan
        prosharerelates = ProjectShare.objects.filter(enviromentcateid = projectshare.enviromentcateid).exclude(projectsharetopicid=projectshare.projectsharetopicid).order_by('-createdate')
        numrelate = len(prosharerelates)
        if numrelate > 8:
            prosharerelates = prosharerelates[0:8]

        # check like
        checklike = ProjectShareLike.objects.filter(projectsharetopicid=projectshare).filter(accountid =account)



        context = {
            'islog': islog,
            'account': account,
            'projectshare': projectshare,
            'numrep': len(prosharereps),
            'numlike': len(prosharelikes),
            'prosharerelates':prosharerelates,
            'numrelate': numrelate,
            'prosharereps': prosharereps,
            'checklike': len(checklike),
        }
        return render(request, 'userprojectshare/projectsharedetail.html', context)
    else:
        islog = 0
        
        # cmt & like
        prosharereps = ProjectShareReply.objects.filter(projectsharetopicid = projectshare).order_by('-createdate')
        if len(prosharereps) > 5:
            prosharereps = prosharereps[0:5]

        prosharelikes = ProjectShareLike.objects.filter(projectsharetopicid = projectshare)
        
        # dự án liên quan
        prosharerelates = ProjectShare.objects.filter(enviromentcateid = projectshare.enviromentcateid).exclude(projectsharetopicid=projectshare.projectsharetopicid).order_by('-createdate')
        numrelate = len(prosharerelates)
        if numrelate > 8:
            prosharerelates = prosharerelates[0:8]


        context = {
            'islog': islog,
            'projectshare': projectshare,
            'numrep': len(prosharereps),
            'numlike': len(prosharelikes),
            'prosharerelates': prosharerelates,
            'numrelate':numrelate,
            'prosharereps': prosharereps,
        }
        return render(request, 'userprojectshare/projectsharedetail.html', context)

def myprojectshare(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])

        myprojectshares = ProjectShare.objects.filter(accountid = account)

        environmentcates = EnviromentCate.objects.all()
        context = {
            'account': account,
            'environmentcates': environmentcates,
            'myprojectshares': myprojectshares,
        }
        return render(request, 'userprojectshare/myprojectshare.html', context)
    else:
        return redirect('userprojectshare:projectshare')


def projectsharecreate(request): 
    if request.session.has_key('username'):
        environmentcates = EnviromentCate.objects.all()
        account = Account.objects.get(username = request.session['username'])
        
        if request.method == "POST":
            idenvir = request.POST.get('enviromentcateid')
            name = request.POST.get('name')
            des = request.POST.get('des')
            link = request.POST.get('link')
            content = request.POST.get('content')

            try: 
                avatar = request.FILES.get('avatar')
            except:
                avatar = None

            if avatar != None:
                urlavatar = tokenFile(avatar)
            else:
                urlavatar = ''

            projectsharenew = ProjectShare(
                enviromentcateid = EnviromentCate.objects.get(enviromentcateid = idenvir),
                accountid = account,
                projectsharetopicname = name,
                description = des,
                content = content,
                createdate = datetime.now(),
                editdate = datetime.now(),
                viewcount = 0,
                likecount = 0,
                avatar = urlavatar,
                isenable = 1,
                link = link,
                note = '',
            )
            projectsharenew.save()

            return redirect('userprojectshare:myprojectshare')

        context = {
            'account': account,
            'environmentcates': environmentcates,
        }

        return render(request, 'userprojectshare/projectsharecreate.html', context)
    else: 
        return redirect('userprojectshare:projectshare')

def projectshareedit(request, idpro): 
    if request.session.has_key('username'):
        environmentcates = EnviromentCate.objects.all()
        account = Account.objects.get(username = request.session['username'])
        projectshare = ProjectShare.objects.get(projectsharetopicid = idpro)
        projectshare.avatar = projectshare.avatar.replace('/media/','')

        if request.method == "POST":
            idenvir = request.POST.get('enviromentcateid')
            name = request.POST.get('name')
            des = request.POST.get('des')
            link = request.POST.get('link')
            content = request.POST.get('content')

            try: 
                avatar = request.FILES.get('avatar')
            except:
                avatar = None

            if avatar != None:
                urlavatar = tokenFile(avatar)
            else:
                urlavatar = '/media/' + projectshare.avatar

           
            projectshare.enviromentcateid = EnviromentCate.objects.get(enviromentcateid = idenvir)
            projectshare.projectsharetopicname = name
            projectshare.description = des
            projectshare.content = content
            projectshare.editdate = datetime.now()
            projectshare.avatar = urlavatar
            projectshare.link = link
             
            projectshare.save()

            return redirect('userprojectshare:myprojectshare')

        context = {
            'account': account,
            'environmentcates': environmentcates,
            'projectshare': projectshare,
        }

        return render(request, 'userprojectshare/projectshareedit.html', context)
    else: 
        return redirect('userprojectshare:projectshare')



