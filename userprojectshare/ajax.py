from django.shortcuts import render, redirect
from homepage.models import *
from homepage.myfunction import *
from homepage.myclass import *
from django.http import JsonResponse

def ajaxprojectsharenew(request):
    sear = request.GET.get('sear')
    selenv = request.GET.get('selenv')
    page = request.GET.get('page')
    if page =='':
        page=0
    page = int(page)
    # page
    if selenv == '0':
        all_projectshare = ProjectShare.objects.all().order_by('-createdate')
    else:
        all_projectshare = ProjectShare.objects.filter(enviromentcateid=selenv).order_by('-createdate')

    # search
    if sear == '' or sear == None:
        pass
    else:
        all_projectshare = all_projectshare.filter(projectsharetopicname__icontains=sear)
    btnmore = 1
    first = 9*page 
    last = (page+1)*9
    if len(all_projectshare)<last:
        last = len(all_projectshare)
        btnmore = 0
    if first >= len(all_projectshare):
        all_projectshare=[]
    else:
        all_projectshare=all_projectshare[first:last]
    s = ''
    for projectshare in all_projectshare:
        link = '/projectshare/' + str(projectshare.projectsharetopicid) + '/detail'
        temp = ''' <div class="col-md-4 gallery-grid">
									<div class="gallery-grid-effects">
										<div id="nivo-lightbox-demo">      
											<div class="ih-item square effect4 bottom_to_top"><a href=''' + link + ''' data-lightbox-gallery="gallery1" id="nivo-lightbox-demo">
												<div class="img"><img src="''' + projectshare.avatar + '''" alt="img"></div>
												<div class="mask1"></div>
												<div class="mask2"></div>
												<div class="info">
													<h3>''' + projectshare.projectsharetopicname + '''</h3>
												</div></a>
											</div>
										</div>
									</div>
								</div>'''
    
        s += temp
    
    data = {
        'btnmore':btnmore,
        'page':page,
        's': s
    }
    return JsonResponse(data)

def ajaxprojectsharelove(request):
    sear = request.GET.get('sear')
    selenv = request.GET.get('selenv')
    page = request.GET.get('page')
    if page =='':
        page=0
    page = int(page)
    # page
    if selenv == '0':
        all_projectshare = ProjectShare.objects.all().order_by('-viewcount')
    else:
        all_projectshare = ProjectShare.objects.filter(enviromentcateid=selenv).order_by('-viewcount')

    # search
    if sear == '' or sear == None:
        pass
    else:
        all_projectshare = all_projectshare.filter(projectsharetopicname__icontains=sear)
    btnmore = 1
    first = 9*page 
    last = (page+1)*9
    if len(all_projectshare)<last:
        last = len(all_projectshare)
        btnmore = 0
    if first >= len(all_projectshare):
        all_projectshare=[]
    else:
        all_projectshare=all_projectshare[first:last]
    s = ''
    for projectshare in all_projectshare:
        link = '/projectshare/' + str(projectshare.projectsharetopicid) + '/detail'
        temp = ''' <div class="col-md-4 gallery-grid">
									<div class="gallery-grid-effects">
										<div id="nivo-lightbox-demo">      
											<div class="ih-item square effect4 bottom_to_top"><a href=''' + link + ''' data-lightbox-gallery="gallery1" id="nivo-lightbox-demo">
												<div class="img"><img src="''' + projectshare.avatar + '''" alt="img"></div>
												<div class="mask1"></div>
												<div class="mask2"></div>
												<div class="info">
													<h3>''' + projectshare.projectsharetopicname + '''</h3>
												</div></a>
											</div>
										</div>
									</div>
								</div>'''
    
        s += temp
    
    data = {
        'btnmore':btnmore,
        'page':page,
        's': s
    }
    return JsonResponse(data)

def ajaxforlike(request):
    idpro = request.GET.get('idpro', None)
    projectshare = ProjectShare.objects.get(projectsharetopicid = idpro)
    account = Account.objects.get(username=request.session['username'])
    checklike = ProjectShareLike.objects.filter(projectsharetopicid=projectshare).filter(accountid = account)
    # chưa like
    s = ''
    if len(checklike) == 0:
        likenew = ProjectShareLike(
            projectsharetopicid = projectshare,
            accountid = account,
            status = 1,
            isenable = 1,
            note = '',
        )
        likenew.save()
        # chuyển thành nút đã like
        s = ''''<button onclick = functionlike() class="btn_1" style="background: #ff0066"><i class="icon_heart"> </i>Bỏ Tim</button>'''
    
    # đã like
    elif len(checklike) == 1:
        for like in checklike:
            like.delete()
        s = ''' <button onclick = functionlike() class="btn_1" style="background: white;color:#ff0066;border: 2px solid #ff0066; "><i class="icon_heart"> </i>Tặng Tim</button>'''

    countlike = ProjectShareLike.objects.filter(projectsharetopicid=projectshare)
    s1 = ' ' + str(len(countlike))
    data = {
        's': s,
        'countlike': s1,
    }
    return JsonResponse(data)

def ajaxforcomment(request):
    idpro = request.GET.get('idpro', None)
    content = request.GET.get('content', None)
    projectshare = ProjectShare.objects.get(projectsharetopicid = idpro)
    account = Account.objects.get(username=request.session['username'])

    prosharerepnew = ProjectShareReply(
        accountid = account,
        projectsharetopicid = projectshare,
        content = content,
        createdate = datetime.now(),
        editdate = datetime.now(),
        isenable = 1,
        note = ''
    )
    prosharerepnew.save()

    prosharereps = ProjectShareReply.objects.filter(projectsharetopicid = projectshare).order_by('-createdate')
    if len(prosharereps) > 5:
        prosharereps = prosharereps[0:5]

    s = ''
    for prosharerep in prosharereps:
        if account.username == prosharerep.accountid.username:
            vardel = '''<span>|</span>
					    <button onclick = check(''' + str(prosharerep.projectsharereplyid) + ''') class="btn_1" style="background-color:orange"> Xóa</button>'''
        else:
            vardel = ''

        temp = ''' <li style="width:100%">
									<div class="avatar">
										<img src="''' + prosharerep.accountid.avatar + '''" alt="" style="width:90px;height:90px">
									</div>
									<div class="comment_right clearfix" style="width:70%">
										<div class="comment_info">
											Bởi <strong style="color:#33ccff">''' + prosharerep.accountid.username + '''</strong><span>|</span>''' + str(prosharerep.createdate.day) +'''-''' + str(prosharerep.createdate.month) + '''- ''' + str(prosharerep.createdate.year) + '''<span> ''' + vardel +'''</span>										
										</div>
										<p> ''' + prosharerep.content + ''' </p>
									</div>
							</li>'''

        s += temp

    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxfordelcomment(request):
    idrep = request.GET.get('idrep', None)
    # lấy rep => del
    projectsharerep = ProjectShareReply.objects.get(projectsharereplyid = idrep)
    idpro = projectsharerep.projectsharetopicid
    projectsharerep.delete()

    prosharereps = ProjectShareReply.objects.filter(projectsharetopicid = idpro).order_by('-createdate')
    if len(prosharereps) > 5:
        prosharereps = prosharereps[0:5]

    account = Account.objects.get(username=request.session['username'])

    s = ''
    for prosharerep in prosharereps:
        if account.username == prosharerep.accountid.username:
            vardel = '''<span>|</span>
					    <button onclick = check(''' + str(prosharerep.projectsharereplyid) + ''') class="btn_1" style="background-color:orange"> Xóa</button>'''
        else:
            vardel = ''

        temp = ''' <li style="width:100%">
									<div class="avatar">
										<img src="''' + prosharerep.accountid.avatar + '''" alt="" style="width:90px;height:90px">
									</div>
									<div class="comment_right clearfix" style="width:70%">
										<div class="comment_info">
											Bởi <strong style="color:#33ccff">''' + prosharerep.accountid.username + '''</strong><span>|</span>''' + str(prosharerep.createdate.day) +'''-''' + str(prosharerep.createdate.month) + '''- ''' + str(prosharerep.createdate.year) + '''<span> ''' + vardel +'''</span>										
										</div>
										<p> ''' + prosharerep.content + ''' </p>
									</div>
							</li>'''

        s += temp

    data = {
        's': s
    }
    return JsonResponse(data)

def ajaxmyprojectshare(request):
    sear = request.GET.get('sear')
    selenv = request.GET.get('selenv')
    page = request.GET.get('page')
    s = ''
    account = Account.objects.get(username = request.session['username'])
    if page =='':
        page=0
    page = int(page)
    if page == 0 :
        s='''<div class="col-md-4 gallery-grid">
									<div class="gallery-grid-effects">
										<div id="nivo-lightbox-demo">      
											<div class="ih-item square effect4 bottom_to_top"><a href="/projectshare/projectsharecreate" data-lightbox-gallery="gallery1" id="nivo-lightbox-demo">
												<div class="img"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQopnPJFidiIBPrnQ2_6z_3BGs1daSPfvn4Ytm6xXAZoFc7jFvj" style="width:100%;height:100%" alt="img"></div>
												<div class="mask1"></div>
												<div class="mask2"></div>
												<div class="info">
													<h3>Thêm Dự Án</h3>	
												</div></a>
											</div>
										</div>
									</div>
								</div>'''
    # page
    if selenv == '0':
        all_projectshare = ProjectShare.objects.filter(accountid = account)
    else:
        all_projectshare = ProjectShare.objects.filter(accountid = account).filter(enviromentcateid=selenv).order_by('-viewcount')

    # search
    if sear == '' or sear == None:
        pass
    else:
        all_projectshare = all_projectshare.filter(projectsharetopicname__icontains=sear)
    
    btnmore = 1
    first = 9*page 
    last = (page+1)*9
    if len(all_projectshare)<last:
        last = len(all_projectshare)
        btnmore = 0
    if first >= len(all_projectshare):
        all_projectshare=[]
    else:
        all_projectshare=all_projectshare[first:last]
    
    for projectshare in all_projectshare:
        link = '/projectshare/' + str(projectshare.projectsharetopicid) + '/detail'
        temp = ''' <div class="col-md-4 gallery-grid">
									<div class="gallery-grid-effects">
										<div id="nivo-lightbox-demo">      
											<div class="ih-item square effect4 bottom_to_top"><a href=''' + link + ''' data-lightbox-gallery="gallery1" id="nivo-lightbox-demo">
												<div class="img"><img src="''' + projectshare.avatar + '''" alt="img" style="width:100%;height:80%"></div>
												<div class="mask1"></div>
												<div class="mask2"></div>
												<div class="info">
													<h3>''' + projectshare.projectsharetopicname + '''</h3>
                                                
												</div></a>
                                                
											</div>
                                            <div style="width: 316px; height: auto; border: 8px solid #fff; box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);">
                                                    <a href = "/projectshare/''' + str(projectshare.projectsharetopicid) + '''/edit "><i class="icon-pen" style="color:#662d91;font-size:14pt"> </i>Sửa</a>
                                                    <a class="play-icon popup-with-zoom-anim" href="#small-dialog5" onclick="openpop('''+ str(projectshare.projectsharetopicid) +''')"><i class="icon-trash-1" style="color:#ffc107;font-size:14pt" > </i>Xóa</a>
                                            </div>
                                            
										</div>
									</div>
								</div>
                                '''
    
        s += temp
    
    data = {
        'btnmore':btnmore,
        'page':page,
        's': s
    }
    return JsonResponse(data)    

def ajaxfordelprojectshare(request):
    idpro = request.GET.get('idpro', None)
    projectshare = ProjectShare.objects.get(projectsharetopicid = idpro)
    account = Account.objects.get(username = request.session['username'])
    
    # Likes
    prolikes = ProjectShareLike.objects.filter(projectsharetopicid = projectshare)
    for prolike in prolikes:
        prolike.delete()
    
    # ShareRep
    proreps = ProjectShareReply.objects.filter(projectsharetopicid = projectshare)
    for prorep in proreps:
        prorep.delete()
    
    projectshare.delete()

    data = {
       's': True
    }
    return JsonResponse(data)