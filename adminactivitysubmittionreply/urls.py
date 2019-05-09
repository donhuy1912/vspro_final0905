from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminactivitysubmittionreply'

urlpatterns= [
    path(r'', views.index, name='index'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^create$', views.create, name='create'),
    
    url(r'ajax/validate_subjectactivitysubmittionreply/$', views.validate_subjectactivitysubmittionreply, name='validate_subjectactivitysubmittionreply'),
    url(r'ajax/validate_chapteractivitysubmittionreply/$', views.validate_chapteractivitysubmittionreply, name='validate_chapteractivitysubmittionreply'),
    url(r'ajax/validate_lessonactivitysubmittionreply/$', views.validate_lessonactivitysubmittionreply, name='validate_lessonactivitysubmittionreply'),
    url(r'ajax/validate_itemactivitysubmittionreply/$', views.validate_itemactivitysubmittionreply, name='validate_itemactivitysubmittionreply'),
    url(r'ajax/validate_activityactivitysubmittionreply/$', views.validate_activityactivitysubmittionreply, name='validate_activityactivitysubmittionreply'),
]