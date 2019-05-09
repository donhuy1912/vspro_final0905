from django.shortcuts import render, redirect
from homepage.models import Account, Contact,UserDetail
from datetime import datetime

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            contacts = Contact.objects.all()
            for contact in contacts:
                contact.createdate = contact.createdate
                
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                    'userdetail':userdetail,
                    'account':account,
                    'contacts': contacts}
            return render(request, 'admincontact/contact_show.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def create(request):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            if request.method == 'POST':
                contact = Contact( 
                                        accountid=Account.objects.get(accountid = request.POST['accountid']), 
                                        createdate= datetime.now(), 
                                        content= request.POST['content'], 
                                        note=request.POST['note'])
                contact.save()
                return redirect('/admincontact/')
            else:
                accounts = Account.objects.all()
                for account in accounts:
                    account.createdate = account.createdate
                    account.editdate = account.editdate
                userdetail=UserDetail.objects.get(accountid=account)
                context = {
                    'userdetail':userdetail,
                    'account':account,
                    'accounts': accounts}
            return render(request, 'admincontact/contact_create.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def edit(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            contact = Contact.objects.get(contactid=id)
            contact.createdate = contact.createdate
            
            accounts = Account.objects.all()
            for account in accounts:
                account.createdate = account.createdate
                account.editdate = account.editdate
            
            userdetail=UserDetail.objects.get(accountid=account)
            context = {
                'userdetail':userdetail,
                'account':account,
                'contact': contact,
                'accounts': accounts,    
            }

            return render(request, 'admincontact/contact_edit.html', context)
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def us_date_to_iso(us_date):
    return '{2}-{0:>02}-{1:>02}'.format(*us_date.split('/'))

def update(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            contact = Contact.objects.get(contactid=id)
            contact.accountid=Account.objects.get(accountid = request.POST['accountid'])
            contact.createdate=contact.createdate
            contact.content=request.POST['content']
            contact.note=request.POST['note']
            contact.save()
            return redirect('/admincontact/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')

def delete(request, id):
    if request.session.has_key('username'):
        account = Account.objects.get(username = request.session['username'])
        if account.accounttypeid.accounttypeid == 1:
            contact = Contact.objects.get(contactid= id)
            contact.delete()
            return redirect('/admincontact/')
        else:
            return redirect('homepage:index')
    else:
        return redirect('homepage:index')