"""PhytoProm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from ecr.views import index, analyze, api, promoter, protein, transcript, celery

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^analyze/$', analyze, name='analyze'),
    re_path(r'^api/(?P<key>[\w_-]*)/$', api, name='api'),
    re_path(r'^promoter/$', promoter, name='promoter'),
    re_path(r'^protein/$', protein, name='protein'),
    re_path(r'^transcript/$', transcript, name='transcript'),
    re_path(r'^celery/$', celery, name='celery'),
    path('admin/', admin.site.urls),
]
