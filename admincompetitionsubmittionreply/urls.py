from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'admincompetitionsubmittionreply'

urlpatterns= [
    path(r'', views.index, name='index'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^create$', views.create, name='create'),
    
    url(r'ajax/validate_competitioncompetitionsubmittionreply/$', views.validate_competitioncompetitionsubmittionreply, name='validate_competitioncompetitionsubmittionreply'),
]
