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
    url(r'^asset/$', views.asset, name='asset'),
    url(r'^asset/add/$', views.asset_add, name='asset_add'),
    url(r'^asset/edit/$', views.asset_edit, name='asset_edit'),
    url(r'^asset/del/$', views.asset_del, name='asset_del'),
    url(r'^asset/update/$', views.asset_update, name='asset_update'),
    url(r'^aliyunecs/$', views.aliyunecs, name='aliyunecs'),

    url(r'^idc/$', views.idc, name='idc'),
    url(r'^group/list/$', views.group_list, name='group_list'),
    url(r'^group/add/$', views.group_add, name='group_add'),

    url(r'^test/$', views.test, name='test'),
]
