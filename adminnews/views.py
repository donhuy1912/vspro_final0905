from django.shortcuts import render, redirect
from homepage.models import News, EnviromentCate, Account, Subject,UserDetail
from datetime import datetime
from django.http import JsonResponse
from homepage.myfunction import tokenFile
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            newss = News.objects.all()
            for news in newss:
                news.createdate = news.createdate
                news.editdate = news.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'newss': newss}
            return render(request, 'adminnews/news_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
        
def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                # Lấy url của avatar
                try:
                    token_avatar = request.FILES['avatar']
                except:
                    token_avatar = None
                ava = ''
                if token_avatar != None:
                    ava = tokenFile(token_avatar)
                

                news = News( 
                                        accountid = Account.objects.get(accountid = request.POST['accountid']),
                                        enviromentcateid = EnviromentCate.objects.get(enviromentcateid = request.POST['enviromentcateid']),
                                        newsname=request.POST['newsname'], 
                                        createdate= datetime.now(), 
                                        editdate= datetime.now(),
                                        description=request.POST['description'],
                                        content=request.POST['content'],
                                        avatar=ava,
                                        isenable=request.POST['isenable'],  
                                        note=request.POST['note'])
                news.save()
                return redirect('/adminnews/')
            else:
                # subjectparts = SubjectPart.objects.all()
                # for subjectpart in subjectparts:
                #     subjectpart.createdate = subjectpart.createdate
                #     subjectpart.editdate = subjectpart.editdate

                enviromentcates = EnviromentCate.objects.all()
                for enviromentcate in enviromentcates:
                    enviromentcate.createdate = enviromentcate.createdate
                    enviromentcate.editdate = enviromentcate.editdate
                
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
                    # 'subjectparts': subjectparts,
                    'enviromentcates': enviromentcates,
                }   
            
            return render(request, 'adminnews/news_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            news = News.objects.get(newsid=id)
            news.createdate = news.createdate
            news.editdate = datetime.now()

            # subjectparts = SubjectPart.objects.all()
            # for subjectpart in subjectparts:
            #     subjectpart.createdate = subjectpart.createdate
            #     subjectpart.editdate = subjectpart.editdate

            enviromentcates = EnviromentCate.objects.all()
            for enviromentcate in enviromentcates:
                enviromentcate.createdate = enviromentcate.createdate
                enviromentcate.editdate = enviromentcate.editdate

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
                'news': news,
                # 'subjectparts': subjectparts,
                'enviromentcates': enviromentcates,
            }
        
            return render(request, 'adminnews/news_edit.html', context)
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
            news = News.objects.filter(newsid = id).update(accountid = Account.objects.get(accountid = getNum(request.POST['accountid'])))
            news = News.objects.filter(newsid = id).update(enviromentcateid = EnviromentCate.objects.get(enviromentcateid = getNum(request.POST['enviromentcateid'])))
            news = News.objects.get(newsid=id)

            # Lấy url của avatar
            try:
                token_avatar = request.FILES['avatar']
            except:
                token_avatar = None
            ava = ''
            if token_avatar != None:
                ava = tokenFile(token_avatar)
            else:
                ava = news.avatar

            news.newsname=request.POST['newsname']
            news.createdate=news.createdate
            news.editdate=datetime.now()
            news.isenable=ava
            news.description=request.POST['description']
            news.content=request.POST['content']
            news.isenable=request.POST['isenable']
            news.note=request.POST['note']
            news.save()
            return redirect('/adminnews/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            news = News.objects.get(newsid= id)
            news.delete()
            return redirect('/adminnews/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


#lấy giá trị subject được nhập vào để giới hạn giá trị show ra của subjectpart
# def validate_subjectnews(request):
#     subject = request.GET.get('subject', None)
#     subjectparts = SubjectPart.objects.filter(subjectid=subject)
#     edit = request.GET.get('edit', False)
#     if edit == '1': 
#         edit = True
    
#     change = request.GET.get('change', False)
#     if change == '1': 
#         change = True
        
#     if edit == True:
#         news  = News.objects.get(newsid = request.GET.get('news', None))
        
#     if edit == False or change == True:
#         s = '<option type="text" name="subjectpartid" value="">-- Chọn --</option>'
#     else:
#         if change == False:
#             s= ' <option type="text" name="subjectpartid" value="' + str(news.subjectpartid.subjectpartid) + ' ">' + news.subjectpartid.subjectpartname + '</option>'
    
#     temp = ''

#     for subjectpart in subjectparts: 
#         if edit == True and change == False:
#             if subjectpart.subjectpartid != news.subjectpartid.subjectpartid:
#                     temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         else:
#             temp = ' <option type="text" name="subjectpartid" value="' + str(subjectpart.subjectpartid) + ' ">' + subjectpart.subjectpartname + '</option>'
#         s = s+temp

#     data = {
#         'is_taken': s
#     }

#     return JsonResponse(data)