from django.urls import path
from . import views
from . import ajax
from django.conf.urls import url


app_name = 'userforum'

urlpatterns = [
    path('userforum/', views.userforum, name = 'userforum'),
    path('userforumblog/<int:id>/', views.userforumblog, name = 'userforumblog'),
    path('userforumpost/', views.userforumpost, name = 'userforumpost'),
    path('fastchat/', views.fastchat, name = 'fastchat'),
    path('myuserforum/<int:id>/', views.myuserforum, name = 'myuserforum'),
    path('myuserforumpost/<int:id>/', views.myuserforumpost, name = 'myuserforumpost'),
    path('myuserforumedit/<int:idacc>/forum/<int:idfor>/', views.myuserforumedit, name = 'myuserforumedit'),

    # url(r'^ajax/forumsearch/$', ajax.ajaxSearchFor, name='forumsearch'),
    url(r'^ajax/forumshow/$', ajax.ajaxShowFor, name='forumshow'),
    url(r'^ajax/forumlike/$', ajax.ajaxLikeFor, name='forumlike'),
    url(r'^ajax/forumunlike/$', ajax.ajaxUnLikeFor, name='forumunlike'),
    # url(r'^ajax/forumreplydelete/$', ajax.ajaxDelCommentFor, name='forumreplydelete'),
    # url(r'^ajax/forumreplycreate/$', ajax.ajaxCreateCommentFor, name='forumreplycreate'),
    url(r'^ajax/forumreplyshow/$', ajax.ajaxShowCommentFor, name='forumreplyshow'),
    # url(r'^ajax/forumsearchofme/$', ajax.ajaxSearchForOfMe, name='forumsearchofme'),
    url(r'^ajax/forumshowofme/$', ajax.ajaxShowForOfMe, name='forumshowofme'),
    # url(r'^ajax/forumdelete/$', ajax.ajaxDelFor, name='forumdelete'),

    path('ajax/chatsent/', ajax.chatsent, name='chatsent'),
    path('ajax/requestchat/', ajax.requestchat, name='requestchat'),
    
]