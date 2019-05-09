from django.urls import path
from . import views
from . import ajax

app_name = 'usergame'

urlpatterns = [
    path('gamelist/sub/<int:idsub>', views.gamelist, name='gamelist'),
    path('game/<int:idgame>/detail', views.gamedetail, name = 'gamedetail'),
    path('game/<int:idgame>/play',views.gameplay, name ='gameplay'),
    path('teachergamelist/sub/<int:idsub>', views.teachergamelist, name='teachergamelist'),
    path('teachergamelist/sub/<int:idsub>/create', views.teachergamecreate, name='teachergamecreate'),
    path('teachergamelist/sub/<int:idsub>/edit/<int:idgame>', views.teachergameedit, name='teachergameedit'),
    
    path('ajax/ajaxforrate', ajax.ajaxforrate),

    path('ajax/ajaxfordelgame',ajax.ajaxfordelgame)
]
