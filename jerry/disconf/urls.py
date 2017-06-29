"""jerry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views

urlpatterns = [
    #url(r'^$', views.cmdb, name='cmdb'),
    url(r'^ansible/file/$', views.ansible_file, name='ansiblefile'),
    url(r'^ansible/run/$', views.ansible_run, name='ansiblerun'),
    url(r'^ansible/job/run/$', views.ansible_job_run, name='ansiblejobrun'),
    url(r'^ansible/job/add/$', views.ansible_job_add, name='ansiblejobadd'),

]
