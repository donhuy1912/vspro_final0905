"""CourseProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path, include


from django.conf.urls import url
from ckeditor_uploader import views as uploader_views 
from django.views.decorators.http import require_http_methods # Khử decorate staff
from django.views.decorators.cache import never_cache # Load hình đã upload


 
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('homepage.urls')),
    path('', include('course.urls')),
	
    # Module
    path('', include('userforum.urls')),
    path('', include('usercompetition.urls')),
    path('', include('userprojectshare.urls')),
    path('', include('usergame.urls')),
    path('', include('usernews.urls')),
   
    # Ckeditor
    url(r'^ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/',never_cache(uploader_views.browse), name='ckeditor_browse'),

    # Admin
	# AdminPage
    path('', include('adminpage.urls')),
    path('adminintroduction/', include('adminintroduction.urls')),
    path('adminheader/', include('adminheader.urls')),
    path('adminfooter/', include('adminfooter.urls')),
    path('adminhome/', include('adminhome.urls')),
    path('adminsliderunbar/', include('adminsliderunbar.urls')),
    path('adminaccounttype/', include('adminaccounttype.urls')),
    path('adminaccount/', include('adminaccount.urls')),
    path('adminuserdetail/', include('adminuserdetail.urls')),
    path('adminenviromentcate/', include('adminenviromentcate.urls')),
    path('adminsubject/', include('adminsubject.urls')),
    path('adminsubjectteacher/', include('adminsubjectteacher.urls')),
    path('adminsubjectpart/', include('adminsubjectpart.urls')),
    path('adminchapter/', include('adminchapter.urls')),
    path('adminlesson/', include('adminlesson.urls')),
    path('adminitem/', include('adminitem.urls')),
    path('adminactivitytype/', include('adminactivitytype.urls')),
    path('adminactivity/', include('adminactivity.urls')),
    path('adminactivitysubmittion/', include('adminactivitysubmittion.urls')),
    path('adminforum/', include('adminforum.urls')),
    path('adminprojectshare/', include('adminprojectshare.urls')),
    path('adminnews/', include('adminnews.urls')),
    path('admincompetition/', include('admincompetition.urls')),
    path('admincompetitionsubmittion/', include('admincompetitionsubmittion.urls')),
    path('adminenrollment/', include('adminenrollment.urls')),
    path('adminsubjectlike/', include('adminsubjectlike.urls')),
    path('adminlessonreply/', include('adminlessonreply.urls')),
    path('adminactivityreply/', include('adminactivityreply.urls')),
    path('adminactivitysubmittionreply/', include('adminactivitysubmittionreply.urls')),
    path('admintracking/', include('admintracking.urls')),
    path('adminforumlike/', include('adminforumlike.urls')),
    path('adminforumreply/', include('adminforumreply.urls')),
    path('adminnewsreply/', include('adminnewsreply.urls')),
    path('adminprojectsharelike/', include('adminprojectsharelike.urls')),
    path('adminprojectsharereply/', include('adminprojectsharereply.urls')),
    path('admincompetitionsubmittionlike/', include('admincompetitionsubmittionlike.urls')),
    path('admincompetitionsubmittionreply/', include('admincompetitionsubmittionreply.urls')),
    path('adminuserrank/', include('adminuserrank.urls')),
    path('admincontact/', include('admincontact.urls')),
    path('adminfastchat/', include('adminfastchat.urls')),
    path('admingametype/', include('admingametype.urls')),
    path('admingamerate/', include('admingamerate.urls')),
    path('admingame/', include('admingame.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)