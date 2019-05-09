from django.shortcuts import render, redirect
from homepage.models import *
from datetime import datetime
from django.contrib import messages
from homepage.myfunction import *
from adminpage import templates
import re
import string


# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userdetails = UserDetail.objects.all()

            for userdetail in userdetails:
                try: 
                   	userdetail.birthday = userdetail.birthday.strftime("%Y-%m-%d")
                except:
                	pass

            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'userdetails': userdetails}
        
            return render(request, 'adminuserdetail/userdetail_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
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
                'accounts':accounts
            }

            if request.method == "POST":
                accountid = request.POST.get('accountid')
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                birthday = request.POST.get('birthday')
                address = request.POST.get('address')
                phonenumber = request.POST.get('phonenumber')
                email = request.POST.get('email')
                isenable = request.POST.get('isenable')
                note = request.POST.get('note')

                if (firstname == '' or lastname =='' or email =='' or phonenumber == '' or accountid == '' or birthday == '' or address == ''):
                    messages.error(request, 'Vui lòng điền đầy đủ các thông tin dấu *')
                    return render(request, 'adminuserdetail/userdetail_create.html', context)
                elif (not isEmail(email)):
                    messages.error(request, 'Email không hợp lệ')
                    return render(request, 'adminuserdetail/userdetail_create.html', context)
                elif (not boolcheckphoneNumber(phonenumber)):
                    messages.error(request, 'Số điện thoại không hợp lệ')
                    return render(request, 'adminuserdetail/userdetail_create.html', context)
                # elif (boolcheckEmail(email)):
                #     messages.error(request, 'Email này đã được sử dụng cho tài khoản khác')
                #     return render(request, 'adminuserdetail/userdetail_create.html', context)
                else:
                    if request.method == 'POST':
                        userdetail = UserDetail( 
                                                    accountid = Account.objects.get(accountid = accountid),
                                                    firstname = firstname, 
                                                    lastname = lastname, 
                                                    birthday =  birthday,
                                                    address = address, 
                                                    phonenumber = phonenumber, 
                                                    email = email, 
                                                    isenable = isenable,
                                                    note = note)
                        userdetail.save()
                        return redirect('/adminuserdetail/')
            
            return render(request, 'adminuserdetail/userdetail_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userdetail = UserDetail.objects.get(userdetailid = id)
            try: 
                userdetail.birthday = userdetail.birthday.strftime("%Y-%m-%d")
            except:
                pass

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            context = {
                'userdetail': userdetail,
                'accounts': accounts
            }

            return render(request, 'adminuserdetail/userdetail_edit.html', context)
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
            userdetail = UserDetail.objects.get(userdetailid = id)
            try: 
                userdetail.birthday = userdetail.birthday.strftime("%Y-%m-%d")
            except:
                pass

            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            context = {
                'userdetail': userdetail,
                'accounts': accounts
            }

            if request.method == "POST":
                accountid = request.POST.get('accountid')
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                birthday = request.POST.get('birthday')
                address = request.POST.get('address')
                email = request.POST.get('email')
                phonenumber = request.POST.get('phonenumber')
                isenable = request.POST.get('isenable')
                note = request.POST.get('note')
            
                if (firstname == '' or lastname =='' or email =='' or phonenumber == ''):
                    messages.error(request, 'Vui lòng điền đầy đủ các thông tin dấu *')
                    return redirect('/adminuserdetail/edit/'+id)
                elif (not isEmail(email)):
                    messages.error(request, 'Email không hợp lệ')
                    return redirect('/adminuserdetail/edit/'+id)
                elif (not boolcheckphoneNumber(phonenumber)):
                    messages.error(request, 'Số điện thoại không hợp lệ')
                    # return render(request, 'adminuserdetail/userdetail_edit.html', context)
                    # x= '/userdetail/edit/'+id
                    return redirect('/adminuserdetail/edit/'+id)
                else:
                    userdetail = UserDetail.objects.filter(userdetailid = id).update(accountid = Account.objects.get(accountid = getNumber(accountid)))
                    userdetail = UserDetail.objects.get(userdetailid = id)
                    userdetail.firstname = firstname
                    userdetail.lastname = lastname
                    userdetail.birthday = birthday
                    userdetail.address = address
                    userdetail.phonenumber = phonenumber
                    userdetail.email = email
                    userdetail.isenable = isenable
                    userdetail.note = note
                    userdetail.save()
                    return redirect('/adminuserdetail/')
            return render(request, 'adminuserdetail/userdetail_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')


def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            userdetail = UserDetail.objects.get(userdetailid =  id)
            userdetail.delete()
            return redirect('/adminuserdetail/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')
