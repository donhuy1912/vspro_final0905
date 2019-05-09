from django.urls import path
from . import views
from . import ajax

app_name = "userprojectshare"

urlpatterns = [
    path('projectshare', views.projectshare, name='projectshare'),
    path('projectshare/allnew', views.projectsharenew, name= 'projectsharenew'),
    path('projectshare/alllove', views.projectsharelove, name= 'projectsharelove'),
    path('projectshare/<int:idpro>/detail', views.projectsharedetail, name="projectsharedetail"),
    path('projectshare/myprojectshare', views.myprojectshare, name= 'myprojectshare'),
    path('projectshare/projectsharecreate', views.projectsharecreate, name= 'projectsharecreate'),
    path('projectshare/<int:idpro>/edit', views.projectshareedit, name= 'projectshareedit'),

    path('ajax/ajaxprojectsharebest', ajax.ajaxprojectsharenew),
    path('ajax/ajaxprojectsharebestlove', ajax.ajaxprojectsharelove),
    path('ajax/ajaxforlike', ajax.ajaxforlike),
    path('ajax/ajaxforcomment', ajax.ajaxforcomment),
    path('ajax/ajaxfordelcomment', ajax.ajaxfordelcomment),
    path('ajax/ajaxmyprojectshare', ajax.ajaxmyprojectshare),
    path('ajax/ajaxfordelprojectshare', ajax.ajaxfordelprojectshare),

]
