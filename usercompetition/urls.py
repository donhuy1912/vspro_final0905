from django.urls import path
from . import views
from . import ajax

app_name = 'usercompetition'

urlpatterns = [
    path('competition', views.competition, name='competition'),
    path('competition/popular', views.competitionpopular, name='competitionpopular'),
    path('competition/<int:idcom>/detail', views.competitiondetail, name='competitiondetail'),
    path('competition/<int:idenvir>/environmentcate', views.competitionenvironment, name='competitionenvironment'),
    path('competition/up/<int:number>', views.competitionbylikeup, name="competitionbylikeup"),
    path('competition/under', views.competitionbylikeunder100, name='competitionbylikeunder100'),
    path('competiton/<int:idcom>/rank', views.competitionlistrank, name='competitionlistrank'),
    path('compettion/<int:idsubmit>/submit', views.competitionsubmitiondetail, name="competitionsubmitiondetail"),
    path('competition/createnew', views.competitioncreate, name="competitioncreate"),
    path('competition/listcompetition', views.listcompetition, name='listcompetition'),
    path('competition/listcompetition/more', views.listcompetition2, name='listcompetition2'),
    path('competition/<int:idcom>/edit', views.competitionedit, name ="competitionedit"),


    path('ajax/submit', ajax.ajaxsubmit),
    path('ajax/ajaxcomment', ajax.ajaxcomment),
    path('ajax/ajaxlikecomsub', ajax.ajaxlikecomsub),
    path('ajax/ajaxpubcom', ajax.ajaxpubcom),
    path('ajax/ajaxdelcom', ajax.ajaxdelcom),
]