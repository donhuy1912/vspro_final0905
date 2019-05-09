from django.shortcuts import render, redirect
from homepage.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homepage.myclass import GamePopNew, GameAndRate
import operator
from homepage.myfunction import tokenFile
from zipfile import ZipFile
from datetime import datetime

# Create your views here.
def gamelist(request,idsub):
    subject=Subject.objects.get(subjectid=idsub)
    allgame = Game.objects.filter(subjectid=idsub)
    arrRate = []
    for game in allgame:
        rates = GameRate.objects.filter(gameid = game)
        temp = GameAndRate(game, len(rates), game.viewcount, game.createdate)
        arrRate.append(temp)

    if (len(arrRate) > 0):
        populargame = sorted(arrRate, key=operator.attrgetter('view'), reverse = True)
        newgame = sorted(arrRate, key=operator.attrgetter('date'), reverse = True)
        
    # populargame = allgame.order_by('-viewcount')
    # newgame = allgame.order_by('-createdate')

    num = len(allgame)
    listgame = []
    if num > 0:
        for i in range(0,num):
            temp = GamePopNew(populargame[i], newgame[i])
            listgame.append(temp)

    paginator = Paginator(listgame, 3) 
    page = request.GET.get('page')
    listgame = paginator.get_page(page)

    if request.session.has_key('username'):

        account = Account.objects.get(username = request.session['username'])
        islog = 1
        context = {
            'islog': islog,
            'account': account,
            'listgame': listgame,
            'subject':subject
        }
        return render(request, 'usergame/gamelist.html', context)
    else:
        islog = 0
        context = { 
            'islog':islog,
            'listgame':listgame,
            'subject':subject
        }
        return render(request, 'usergame/gamelist.html', context)

def gamedetail(request, idgame):
    if request.session.has_key('username'):
        game = Game.objects.get(gameid = idgame)
        game.viewcount += 1
        game.save()
        sumrate=0
        gamerates= GameRate.objects.filter(gameid=game).order_by('-createdate')
        for gamerate in gamerates:
            sumrate+= gamerate.rate
        countrate=len(gamerates)
        if countrate > 0:
            avgrate = round(sumrate/countrate, 2)
        else:
            countrate=0
            avgrate = 0
        account = Account.objects.get(username = request.session['username'])
        
        # Người đánh giá gần đây
        if len(gamerates) > 5:
            playerrates = gamerates[0:5]
        else:
            playerrates = gamerates
        # Tro choi lien quan
        gamerelates = Game.objects.filter(subjectid = game.subjectid).exclude(gameid = game.gameid).order_by('-createdate')
        
        if len(gamerelates) > 5:
            gamerelates = gamerelates[0:5]


        context = {
            'account': account,
            'avgrate':avgrate,
            'countrate':countrate,
            'game':game,
            'gamerelates': gamerelates,
            'playerrates': playerrates,
        }

       
        return render(request, 'usergame/gamedetail.html', context)
        
    else:
        game = Game.objects.get(gameid = idgame)
        return redirect('usergame:gamelist', game.subjectid.subjectid)

def gameplay(request, idgame):
    if request.session.has_key('username'):
        game = Game.objects.get(gameid = idgame)
        account = Account.objects.get(username = request.session['username'])
        
        context = {
            'account': account,
            'game':game 
        }

        if game.gametypeid.gametypeid ==1:
            return render(request, 'usergame/gameplay.html', context)
        elif game.gametypeid.gametypeid ==2:
            return render(request, 'usergame/gameplay2.html', context)
            
    else:
        return redirect('usergame:gamedetail', game.gameid)

def teachergamelist(request, idsub):
    subject=Subject.objects.get(subjectid=idsub)
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        allgame = Game.objects.filter(subjectid=idsub).filter(accountid=account)
        arrRate = []
        for game in allgame:
            rates = GameRate.objects.filter(gameid = game)
            temp = GameAndRate(game, len(rates), game.viewcount, game.createdate)
            arrRate.append(temp)

        if (len(arrRate) > 0):
            populargame = sorted(arrRate, key=operator.attrgetter('view'), reverse = True)
            newgame = sorted(arrRate, key=operator.attrgetter('date'), reverse = True)
            
        # populargame = allgame.order_by('-viewcount')
        # newgame = allgame.order_by('-createdate')

        num = len(allgame)
        listgame = []
        if num > 0:
            for i in range(0,num):
                temp = GamePopNew(populargame[i], newgame[i])
                listgame.append(temp)

        paginator = Paginator(listgame, 3) 
        page = request.GET.get('page')
        listgame = paginator.get_page(page)

        context = {
            'account': account,
            'listgame': listgame,
            'subject':subject
        }
        return render(request, 'usergame/teachergamelist.html', context)
    else:
        return redirect('homepage:index')

def teachergamecreate(request,idsub):
    
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2:
            gametypes = GameType.objects.all()
        
            if request.method == "POST":
                gametype = request.POST.get('gametype')
                name = request.POST.get('name')
                des = request.POST.get('des')
                try: 
                    avatar = request.FILES.get('avatar')
                except:
                    avatar = None
                
                if avatar != None:
                    urlavatar = tokenFile(avatar)
                else:
                    urlavatar = ''
                
                content = request.POST.get('content')

                linkneed = ''

                if gametype == '1':
                    try:
                        scorm = request.FILES.get('scorm')
                    except:
                        scorm = None
                    
                    if scorm != None:
                        urlscorm = tokenFile(scorm)
                    else:
                        urlscorm = ''

                    nameScorm = urlscorm

                    if nameScorm != '':
                        nameScorm = nameScorm.replace('/media/','')
                        nameScorm = nameScorm.replace('.zip','')
                        s = '.' + urlscorm
                        # s = '.'
                        # m = "\\"
                        # for i in urlscorm:
                        #     if i == '/':
                        #         s += m
                        #     else:
                        #         s += i

                        unzip = ZipFile(s)
                        urlunzip='./media/unzip/' + nameScorm
                        unzip.extractall(urlunzip)
                        unzip.close
                        nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                        linkneed = nameScorm


                elif gametype == '2':
                    link = request.POST.get('link')
                    linkneed = link

                gamenew = Game(
                    gametypeid = GameType.objects.get(gametypeid=gametype),
                    accountid = account,
                    subjectid = Subject.objects.get(subjectid = idsub),
                    gamename = name,
                    description = des,
                    content = content,
                    avatar = urlavatar,
                    createdate =datetime.now(),
                    editdate = datetime.now(),
                    viewcount = 0,
                    link = linkneed,
                )
                
                gamenew.save()
                
                return redirect("usergame:teachergamelist", idsub=idsub )

            context = {
                        'gametypes':gametypes,
                        'account': account,
                    }
        
            return render(request, 'usergame/gamecreate.html',context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def teachergameedit(request,idsub,idgame):
    
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        game = Game.objects.get(gameid=idgame)
        if account.accountid == game.accountid.accountid :
            if account.accounttypeid.accounttypeid == 1 or account.accounttypeid.accounttypeid == 2:
                gametypes = GameType.objects.all()
            
                if request.method == "POST":
                    
                    name = request.POST.get('name')
                    des = request.POST.get('des')
                    try: 
                        avatar = request.FILES.get('avatar')
                    except:
                        avatar = None
                    
                    if avatar != None:
                        urlavatar = tokenFile(avatar)
                    else:
                        urlavatar = game.avatar
                    
                    content = request.POST.get('content')


                    linkneed = ''
                    if game.gametypeid.gametypeid == 1:
                        try:
                            scorm = request.FILES.get('scorm')
                        except:
                            scorm = None
                        
                        if scorm != None:
                            urlscorm = tokenFile(scorm)
                        else:
                            urlscorm = game.link

                        nameScorm = urlscorm

                        if nameScorm != game.link:
                            nameScorm = nameScorm.replace('/media/','')
                            nameScorm = nameScorm.replace('.zip','')
                            s = '.' + urlscorm
                           

                            unzip = ZipFile(s)
                            urlunzip='./media/unzip/' + nameScorm
                            unzip.extractall(urlunzip)
                            unzip.close
                            nameScorm = '/media/unzip/'+ nameScorm + '/story_flash.html'
                            
                        linkneed = nameScorm


                    elif game.gametypeid.gametypeid == 2:
                        link = request.POST.get('link')
                        linkneed = link

                      
                    game.gamename = name
                    game.description = des
                    game.content = content
                    game.avatar = urlavatar
                    game.editdate = datetime.now()   
                    game.link = linkneed
  
                    game.save()
                    
                    return redirect("usergame:teachergamelist", idsub=idsub )
                scormurl=game.link.replace("/media/unzip/",'').replace("/story_flash.html","")
                scormurl+='.zip'
                avaurl = game.avatar.replace("/media/","")
                context = {
                            'scormurl':scormurl,
                            'gametypes':gametypes,
                            'account': account,
                            'game': game,
                            'avaurl':avaurl,
                        }
            
                return render(request, 'usergame/gameedit.html',context)
            else:
                return redirect('homepage:index')
        else:
             return redirect('homepage:index')
    else:
        return redirect('homepage:index')
