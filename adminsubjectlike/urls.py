from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminsubjectlike'

urlpatterns= [
    path(r'', views.index, name='index'),
    url(r'^subjectlike/delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^subjectlike/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^subjectlike/edit/update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^subjectlike/create$', views.create, name='create'),
]
