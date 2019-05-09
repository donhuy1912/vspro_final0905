from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminactivityreply'

urlpatterns= [
    path(r'', views.index, name='index'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^create$', views.create, name='create'),
    
    url(r'^ajax/validate_subjectactivityreply/$', views.validate_subjectactivityreply, name='validate_subjectactivityreply'),
    url(r'^ajax/validate_chapteractivityreply/$', views.validate_chapteractivityreply, name='validate_chapteractivityreply'),
    url(r'^ajax/validate_lessonactivityreply/$', views.validate_lessonactivityreply, name='validate_lessonactivityreply'),
    url(r'^ajax/validate_itemactivityreply/$', views.validate_itemactivityreply, name='validate_itemactivityreply'),
    
]