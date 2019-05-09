from django.shortcuts import render, redirect
from homepage.models import *
from datetime import datetime
from homepage.myfunction import *
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
# def admin1 (request):
#     return render(request, 'account/account_create.html')

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounts = Account.objects.all()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounts': accounts
                }
            return render(request, 'adminaccount/account_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounttypes = AccountType.objects.all()
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounttypes': accounttypes
                }


            if request.method == "POST":
                accounttypeid = request.POST.get('accounttypeid')
                username = request.POST.get('username')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                # resetcode = request.POST.get('resetcode')
                isenable = request.POST.get('isenable') 
                note = request.POST.get('note')
                
                if (boolcheckSpace(username) or boolcheckSpace(password1)):
                    messages.error(request, 'Không được có khoảng trắng trong tên đăng nhập hoặc mật khẩu')
                    return render(request, 'adminaccount/account_create.html', context)
                elif boolcheckUser(username):
                    messages.error(request, 'Tên đăng nhập đã tồn tại')
                    return render(request, 'adminaccount/account_create.html', context)
                elif not (boolcheckPassword(password1)):
                    messages.error(request, 'Mật khẩu phải dài hơn 8 ký tự bao gồm chữ hoa, chữ thường và số')
                    return render(request, 'adminaccount/account_create.html', context)
                elif (password1 != password2):
                    messages.error(request, 'Mật khẩu không trùng khớp')
                    return render(request, 'adminaccount/account_create.html', context)
                else:
                    # Lấy avatar
                    try:
                        token_avatar = request.FILES['avatar']
                    except:
                        token_avatar = None
                    ava = 'media/userava.png'
                    if tokenFile(token_avatar) != None:
                        ava = tokenFile(token_avatar)
                                
                    account = Account( 
                                        accounttypeid = AccountType.objects.get(accounttypeid =  accounttypeid),
                                        username = username,
                                        password = hashPassword(password1), 
                                        createdate =  datetime.now(), 
                                        editdate =  datetime.now(),
                                        avatar = ava,
                                        # resetcode = resetcode,
                                        isenable = isenable,  
                                        note =  note)
                    account.save()
                    return redirect('/adminaccount/')
                
            return render(request, 'adminaccount/account_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        acc = Account.objects.get(username = request.session['username'])
        if acc.accounttypeid.accounttypeid == 1:
            account = Account.objects.get(accountid = id)
            account.createdate = account.createdate
            account.editdate = datetime.now()


            accounttypes = AccountType.objects.all()
            userdetail=UserDetail.objects.get(accountid=acc)
            context = {
                    'userdetail':userdetail,
                    'acc':acc,
                    'account':account,
                    'accounttypes': accounttypes}
            return render(request, 'adminaccount/account_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def us_date_to_iso(us_date):
    return '{2}-{0:>02}-{1:>02}'.format(*us_date.split('/'))

def getNumber(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'accounts': accounts
            }

            account = Account.objects.get(accountid = id)
            if request.method == 'POST':
                accounttypeid = request.POST.get('accounttypeid')
                username = request.POST.get('username')
                # password1 = request.POST.get('password1')
                # password2 = request.POST.get('password2')
                # avatar = request.POST['avatar']
                isenable = request.POST.get('isenable') 
                note = request.POST.get('note')
                
                if boolcheckSpace(username):
                    messages.error(request, 'Không được có khoảng trắng trong tên đăng nhập hoặc mật khẩu')
                    return redirect('/adminaccount/edit/'+id)
                elif (account.username != username and boolcheckUser(username)):
                    messages.error(request, 'Tên đăng nhập đã tồn tại')
                    return redirect('/adminaccount/edit/'+id)
                # elif account.password != password1 and (not (boolcheckPassword(password1))):
                #     messages.error(request, 'Mật khẩu phải dài hơn 8 ký tự bao gồm chữ hoa, chữ thường và số')
                #     return redirect('/adminaccount/edit/'+id)
                # elif password1 != password2:
                #     messages.error(request, 'Mật khẩu không trùng khớp')
                #     return redirect('/adminaccount/edit/'+id)
                else:
                    try:
                        token_avatar = request.FILES['avatar']
                    except:
                        token_avatar = None
                    ava = ''
                    if token_avatar != None:
                        ava = tokenFile(token_avatar)
                    else:
                        ava = account.avatar
                    account = Account.objects.filter(accountid = id).update(accounttypeid = AccountType.objects.get(accounttypeid = getNumber(accounttypeid)))
                    account = Account.objects.get(accountid = id)
                    if account.username != username:
                        account.username = username
                    # if account.password != password1:
                    #     account.password = hashPassword(password1)
                    account.createdate = account.createdate
                    account.editdate = datetime.now()
                    account.avatar = ava
                    # account.resetcode = resetcode
                    account.isenable = isenable
                    account.note = note
                    account.save()
                    return redirect('/adminaccount/')
            return render(request, 'adminaccount/account_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')    
    
def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            account = Account.objects.get(accountid =  id)
            account.delete()
            return redirect('/adminaccount/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')  