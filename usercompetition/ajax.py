from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myfunction import *
from homepage.myclass import *
from django.http import JsonResponse

def ajaxsubmit(request):
    comsubmit = request.GET.get('comsubmitname', None)
    link = request.GET.get('link', None)
    des = request.GET.get('des', None)
    idcom = request.GET.get('idcom', None)
    competition = Competition.objects.get(competitionid = idcom)
    account = Account.objects.get(username = request.session['username'])

    checksubmit = CompetitionSubmittion.objects.filter(competitionid = competition).filter(accountid = account)
    if (len(checksubmit) > 0):
        for checksub in checksubmit:
            checksublike = CompetitionSubmittionLike.objects.filter(competitionsubmittionid=checksub)
            for checklike in checksublike:
                checklike.delete()
            checksubrep = CompetitionSubmittionReply.objects.filter(competitionsubmittionid=checksub)
            for checkrep in checksubrep:
                checkrep.delete()
            checksub.delete()
    competitionsubmit = CompetitionSubmittion(
        accountid = account,
        competitionid = competition,
        createdate = datetime.now(),
        editdate = datetime.now(),
        link = link,
        description = comsubmit,
        content = des,
        isenable = 1,
        note = '',
    )
    competitionsubmit.save()

    s = ''
    # Lấy submit theo ngày
    comsubmits = CompetitionSubmittion.objects.filter(competitionid = competition).order_by('-createdate')
    numsubmit = len(comsubmits)
    if numsubmit >= 5:
        loadcomsubmit = comsubmits[0:5]
    else:
        loadcomsubmit = comsubmits[0:numsubmit]

    for submit in loadcomsubmit:
        link =  '/compettion/' + str(submit.competitionsubmittionid) + '/submit'
        temp = '''<li>
						<div style="box-shadow: 2px 10px 5px 5px #888888;padding: 10px 10px 10px 10px;" >
							<div class="avatar" >
								<img src="''' + submit.accountid.avatar + '''" alt="">
							</div>
							<div class="comment_right clearfix" style="width:87%">
								<div class="comment_info" style="width:100%">
									Bởi <strong style="color:#33ccff">''' + submit.accountid.username + '''</strong></a><span>|</span>''' + str(submit.createdate.day) + '''-''' + str(submit.createdate.month) + '''-''' + str(submit.createdate.year) + '''<span>|</span><a href="''' + link + '''">Chi Tiết</a>
										<h4 style="font-family:Arial;color: #ffc107">''' + submit.description + '''</h4>
								</div>			
							</div>
						</div>
				</li>'''
        s += temp

    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxcomment(request):
    idsubmit =  request.GET.get('idsubmit', None)
    des = request.GET.get('des', None)
    submit= CompetitionSubmittion.objects.get(competitionsubmittionid=idsubmit)
    account = Account.objects.get(username = request.session['username'])

    comsubrepsave =CompetitionSubmittionReply(
        competitionsubmittionid =submit,
        accountid=account,
        content=des,
        createdate = datetime.now(),
        editdate = datetime.now(),
        isenable =1,
        note=''
    )
    comsubrepsave.save()
    s=''
    comsubreps = CompetitionSubmittionReply.objects.filter(competitionsubmittionid=idsubmit).order_by('-createdate')
    if len(comsubreps)>=5:    
        comsubreps = comsubreps[0:5]
    else:
        comsubreps = comsubreps[0:len(comsubreps)]
    for comment in comsubreps:
        temp='''<li style="width:100%">
									<div class="avatar">
										<img src="'''+comment.accountid.avatar+'''" alt="" style="width: 150px;height: 150px">
									</div>
									<div class="comment_right clearfix" style="width:70%">
										<div class="comment_info">
											Bởi <strong style="color:#33ccff">'''+comment.accountid.username+'''</strong><span>|</span>'''+ str(comment.createdate.day)+'''-'''+str(comment.createdate.month)+'''-'''+str(comment.createdate.year)+'''<span></span>										
										</div>
										<p>'''+comment.content+'''</p>
									</div>
							</li>'''
        s+=temp
    data={
        's':s
    }
    return JsonResponse(data)

def ajaxlikecomsub(request):
    idsubmit =  request.GET.get('idsubmit', None)
    submit= CompetitionSubmittion.objects.get(competitionsubmittionid=idsubmit)
    account = Account.objects.get(username = request.session['username'])
    listlike = CompetitionSubmittionLike.objects.filter(accountid=account).filter(competitionsubmittionid=submit)
    if len(listlike) > 0:
        for like in listlike:
            like.delete()
        s='''<button class="btn_1" onclick="likefunction()" style="background: white;color: #fcc107;border: 2px solid #fcc107; "><i class="icon_star voted"> </i>Tặng Sao</button>'''
    else:
        comlikenew= CompetitionSubmittionLike(
            competitionsubmittionid=submit,
            accountid=account,
            status=1,
            isenable=1,
            note='',
        )
        comlikenew.save()
        s='''<button class="btn_1" onclick="likefunction()" style="background: #fcc107"><i class="icon_star voted"> </i>Hủy Sao</button>'''
        
    countlike = " "+ str(len(CompetitionSubmittionLike.objects.filter(accountid=account).filter(competitionsubmittionid=submit)))
    
    data={
        's':s,
        'countlike':countlike,
    }
    return JsonResponse(data)

def ajaxpubcom(request):
    idcom = request.GET.get('idcom', None)
    competition = Competition.objects.get(competitionid = idcom)
    account = Account.objects.get(username=request.session['username'])
    if competition.accountid == account:
        competition.isenable = 1
        competition.save()
    data = {
    }
    return JsonResponse(data)

def ajaxdelcom(request):
    idcom = request.GET.get('idcom', None)
    competition = Competition.objects.get(competitionid = idcom)
    account = Account.objects.get(username=request.session['username'])
    if competition.accountid == account and competition.isenable == 0:
        competition.delete()
    data = {
    }
    return JsonResponse(data)



