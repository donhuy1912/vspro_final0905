from django.urls import path
from . import views

app_name = 'adminpage'

urlpatterns = [
    path('adminpage/', views.admin1, name = 'adminpage'),
    path('admin2/', views.admin2, name = 'admin2'),
    
]