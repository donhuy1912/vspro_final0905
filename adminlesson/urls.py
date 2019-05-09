from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminlesson'

urlpatterns= [
    path('', views.index, name='index'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^create$', views.create, name='create'),

    url(r'^ajax/validate_subjectlesson/$', views.validate_subjectlesson, name='validate_subjectlesson'),
    url(r'^ajax/validate_subjectorderlesson/$', views.validate_subjectorderlesson, name='validate_subjectorderlesson'),
    url(r'^ajax/validate_chapterorderlesson/$', views.validate_chapterorderlesson, name='validate_chapterorderlesson'),
]