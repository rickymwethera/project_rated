from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

urlpatterns=[
    path('',views.home, name='home'),
    path('project/new/',views.create_post,name = 'create'),
    path('^search/', views.search_results, name='search'),
    url(r'project/(\d+)',views.detail,name = 'details'),
    path(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)