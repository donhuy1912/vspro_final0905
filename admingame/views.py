from django.shortcuts import render, redirect
from homepage.models import Game, GameType, Subject, Account, UserDetail
from datetime import datetime
from homepage.myfunction import *
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            games = Game.objects.all()
            for game in games:
                game.createdate = game.createdate
                game.editdate = game.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'games': games}
            return render(request, 'admingame/game_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                try:
                    token_avatar = request.FILES['avatar']
                except:
                    token_avatar = None
                ava = ''
                if token_avatar != None:
                    ava = tokenFile(token_avatar)
                game = Game( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        subjectid = Subject.objects.get(subjectid = request.POST['subjectid']),
                                        gametypeid = GameType.objects.get(gametypeid = request.POST['gametypeid']),
                                        gamename=request.POST['gamename'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        viewcount = request.POST['viewcount'],
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        link=request.POST['link'])
                                        
                game.save()
                return redirect('/admingame/')
            else:
                games = Game.objects.all()
                for game in games:
                    game.createdate = game.createdate
                    game.editdate = game.editdate
                
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                
                subjects = Subject.objects.all()
                for subject in subjects:
                    subject.createdate = subject.createdate
                    subject.editdate = subject.editdate
                
                gametypes = GameType.objects.all()
                for gametype in gametypes:
                    gametype.createdate = gametype.createdate
                    gametype.editdate = gametype.editdate
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'games': games,
                    'gametypes': gametypes,
                    'accounts': accounts,
                    'subjects': subjects,
                }
            return render(request, 'admingame/game_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            game = Game.objects.get(gameid=id)
            game.createdate = game.createdate
            game.editdate = datetime.now()
            
            gametypes = GameType.objects.all()
            for gametype in gametypes:
                gametype.createdate = gametype.createdate
                gametype.editdate = gametype.editdate

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
                
            subjects = Subject.objects.all()
            for subject in subjects:
                subject.createdate = subject.createdate
                subject.editdate = subject.editdate

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'game': game,
                'gametypes': gametypes,
                'subjects': subjects,
                'accounts': accounts,
            }
            return render(request, 'admingame/game_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def getNumber(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            game = Game.objects.get(gameid=id)
            try:
                token_avatar = request.FILES['avatar']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = game.avatar

            game.link = game.link
            
            game = Game.objects.filter(gameid = id).update(accountid = Account.objects.get(accountid = getNumber(request.POST['accountid'])))
            game = Game.objects.filter(gameid = id).update(subjectid = Subject.objects.get(subjectid = getNumber(request.POST['subjectid'])))
            game = Game.objects.filter(gameid = id).update(gametypeid = GameType.objects.get(gametypeid = getNumber(request.POST['gametypeid'])))
            game = Game.objects.get(gameid=id)
            game.gamename=request.POST['gamename']
            game.createdate=game.createdate
            game.editdate=datetime.now()
            game.viewcount = request.POST['viewcount']
            game.description=request.POST['description']
            game.content=request.POST['content']
            game.avatar=ava
            game.link=request.POST['link']
            game.save()
            return redirect('/admingame/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            game = Game.objects.get(gameid= id)
            game.delete()
            return redirect('/admingame/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


# #lấy giá trị subject được nhập vào để giới hạn giá trị show ra của chapter
# def validate_subjectactivity(request):
#     subject = request.GET.get('subject', None)
#     chapters = Chapter.objects.filter(subjectid=subject)
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True
        
#     if edit == True:
#         activity  = Activity.objects.get(activityid = request.GET.get('activity', None))
    
#     if edit == False or change == True:
#         s = '<option type="text" name="chapterid" value="">-- Chọn --</option>'
#     else:
#         if change == False:
#             s= ' <option type="text" name="chapterid" value="' + str(activity.itemid.lessonid.chapterid.chapterid) + ' ">' + activity.itemid.lessonid.chapterid.chaptername + '</option>'
    
#     temp = ''

#     for chapter in chapters: 
#         if edit == True and change == False:
#             if chapter.chapterid != activity.itemid.lessonid.chapterid.chapterid:
#                     temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
#         else:
#             temp = ' <option type="text" name="chapterid" value="' + str(chapter.chapterid) + ' ">' + chapter.chaptername + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)




# #lấy giá trị chapter được nhập vào để giới hạn giá trị show ra của lesson
# def validate_chapteractivity(request):
#     chapter = request.GET.get('chapter', None)
#     lessons = Lesson.objects.filter(chapterid=chapter)
    
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True

#     if edit == True:
#         activity  = Activity.objects.get(activityid = request.GET.get('activity', None))

#     if edit == False or change == True:
#         s = '<option type="text" name="lessonid" value="">-- Chọn --</option>'
#     else:
#         s= ' <option type="text" name="lessonid" value="' + str(activity.itemid.lessonid.lessonid) + ' ">' + activity.itemid.lessonid.lessonname + '</option>'
    
#     temp = ''

#     for lesson in lessons: 
#         if edit == True and change == False:
#             if lesson.lessonid!=activity.itemid.lessonid.lessonid:
#                     temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
#         else:
#             temp = ' <option type="text" name="lessonid" value="' + str(lesson.lessonid) + ' ">' + lesson.lessonname + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)

# #lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của item
# def validate_lessonactivity(request):
#     lesson = request.GET.get('lesson', None)
#     items = Item.objects.filter(lessonid=lesson)
    
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True

#     if edit == True:
#         activity  = Activity.objects.get(activityid = request.GET.get('activity', None))

#     if edit == False or change == True:
#         s = '<option type="text" name="itemid" value="">-- Chọn --</option>'
#     else:
#         s= ' <option type="text" name="itemid" value="' + str(activity.itemid.itemid) + ' ">' + activity.itemid.itemname + '</option>'
    
#     temp = ''

#     for item in items: 
#         if edit == True and change == False:
#             if item.itemid!=activity.itemid.itemid:
#                     temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
#         else:
#             temp = ' <option type="text" name="itemid" value="' + str(item.itemid) + ' ">' + item.itemname + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)

# #lấy giá trị lesson được nhập vào để giới hạn giá trị show ra của activity
# def validate_lessonactivityactivity(request):
#     lesson = request.GET.get('lesson', None)
#     items = Item.objects.filter(lessonid=lesson)
    
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True

#     if edit == True:
#         act  = Activity.objects.get(activityid = request.GET.get('activity', None))
       

#     if edit == False or change == True:
#         s = '<option type="text" name="activityid" value="">-- Chọn --</option>'
#         if edit == False:
#             s += '<option type="text" name="activityid" value="">-- Không có --</option>'
#     else:
#         if act.requiredactivityid == None:
#             s ='<option type="text" name="activityid" value="">-- Không có --</option>'   
#         else:
#             s= ' <option type="text" name="activityid" value="' + str(act.requiredactivityid.activityid) + ' ">' + act.requiredactivityid.activityname + '</option>'
    
#     temp = ''

#     for item in items: 
#         activitys = Activity.objects.filter(itemid = item.itemid)
#         for activity in activitys:
#             if edit == True and change == False:
#                 if act.requiredactivityid != None and activity.activityid != act.requiredactivityid.activityid:
#                    temp = '<option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
#             else:
#                 temp = '<option type="text" name="activityid" value="' + str(activity.activityid) + ' ">' + activity.activityname + '</option>'
#             s = s+temp
#     if change == True:
#         s+='<option type="text" name="activityid" value="">-- Không có --</option>'
#     data = {
#         'is_taken': s,
#     }

#     return JsonResponse(data)


# #lấy giá trị item được nhập vào để gán giá trị cho order
# def validate_itemorderactivity(request):
#     item = request.GET.get('item', None)
#     ite = request.GET.get('ite', None)
#     activitys = Activity.objects.filter(itemid=item)
#     act = request.GET.get('act', None)
#     if act != None:
#         act = Activity.objects.get(activityid = act)
    
#     if len(activitys) == 0:
#         s = 1
#     else:
#         listorder=[]
#         if ite != None and item != None and int(ite) == int(item):
#             s = act.order
#         else:
#             for activity in activitys:
#                 listorder.append(activity.order) 
                
#             s=max(listorder) + 1
    
#     data = {
#         'is_taken': s,
#     }

#     return JsonResponse(data)
