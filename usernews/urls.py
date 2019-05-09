from django.urls import path
from . import views
from . import ajax
from django.conf.urls import url


app_name = 'usernews'

urlpatterns = [
    path('usernews/', views.usernews, name = 'usernews'),
    path('usernewsblog/<int:id>/', views.usernewsblog, name = 'usernewsblog'),
    # path('usernewspost/', views.usernewspost, name = 'usernewspost'),
    # path('fastchat/', views.fastchat, name = 'fastchat'),
    path('myusernews/<int:id>/', views.myusernews, name = 'myusernews'),
    path('myusernewspost/<int:id>/', views.myusernewspost, name = 'myusernewspost'),
    path('myusernewsedit/<int:idacc>/news/<int:idnew>/', views.myusernewsedit, name = 'myusernewsedit'),

    url(r'^ajax/newssearch/$', ajax.ajaxSearchNew, name='newssearch'),
    # url(r'^ajax/newsreplydelete/$', ajax.ajaxDelCommentNew, name='newsreplydelete'),
    # url(r'^ajax/newsreplycreate/$', ajax.ajaxCreateCommentNew, name='newsreplycreate'),
    url(r'^ajax/newsreplyshow/$', ajax.ajaxShowCommentNews, name='newsreplyshow'),
    url(r'^ajax/newssearchofme/$', ajax.ajaxSearchNewsOfMe, name='newssearchofme'),
    # url(r'^ajax/newsdelete/$', ajax.ajaxDelNews, name='newsdelete'),
]