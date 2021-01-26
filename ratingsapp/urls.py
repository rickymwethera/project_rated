from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home, name='home'),
    path('project/new/',views.create_post,name = 'create'),
    path('^search/', views.search_results, name='search'),
    url(r'project/(\d+)',views.detail,name = 'details'),
    path(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)