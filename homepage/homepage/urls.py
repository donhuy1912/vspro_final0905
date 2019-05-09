from django.urls import path
from . import views,ajax
from django.conf.urls import url


app_name = 'homepage'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.myLogin, name = 'login'),
    path('logout/', views.myLogout, name = 'logout'),
    path('register/', views.myRegister, name = 'register'),
    
    path('introduction/', views.introduction, name = 'introduction' ),
    path('aboutus/', views.aboutUs, name = 'aboutus'),
	path('vision/', views.vision, name = 'vision'),
    path('resource/', views.resource, name = 'resource'),
    path('userguide/', views.userguide, name = 'userguide'),
    path('sitemap/', views.sitemap, name ="sitemap"),
    path('contact/', views.contact, name = 'contact'),
	path('team/', views.team, name = 'team'),
    path('myprofile/<int:id>/', views.myProfile, name = 'myprofile' ), 
	path('myprofile/<int:id>/changepassword/', views.myChangepassword, name = 'changepassword'),
    path('forgotpassword/', views.passForgot, name = 'forgotpass'),
    path('confirmpassword/', views.passConfirm, name = 'confirmpass'),
    path('activeaccount/', views.activeAccount, name = 'activeaccount'),
    path('confirmaccount/', views.confirmAccount, name =  'confirmaccount'),

    path('userprofile/<int:idguest>/', views.userprofile, name="userprofile"),
    path('search/<str:subname>', views.searchsub, name="search"),
        
    # path('myprofile/<int:id>/', views.myProfile, name = 'myprofile' ),
    path('editprofile/<int:id>/', views.editMyProfile, name = 'editmyprofile' ),

    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    # url(r'^ajax/validate_email/$', views.validate_email, name='validate_email')

    path('adminchat/', views.adminchat, name =  'adminchat'),

    path('ajax/getallroomchat/', ajax.getallroomchat, name="getallroomchat"),
    path('ajax/getallmesadmin/', ajax.getallmesadmin, name="getallmesadmin"),
    path('ajax/getmesadmin/', ajax.getmesadmin, name="getmesadmin"),
    path('ajax/sentmesadmin/', ajax.sentmesadmin, name="sentmesadmin"),

    path('ajax/ajaxsentmes/', ajax.ajaxsentmes, name="ajaxsentmes"),
    path('ajax/getallmes/', ajax.getallmes, name="getallmes"),
    path('ajax/getmes/', ajax.getmes, name="getmes"),
   
    path('ajax/logingmail/', ajax.logingmail, name = 'logingmail'),
    path('ajax/loginfacebook/', ajax.loginfacebook),

    path('ajax/getroombutton/', ajax.getroombutton),
    path('ajax/delmesadmin/', ajax.delmesadmin),
]