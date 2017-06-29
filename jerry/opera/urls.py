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

    url(r'^db_info/$', views.db_info, name='db_info'),
    url(r'^dbtable_info/$', views.dbtable_info, name='dbtable_info'),
    url(r'^dbinfo_remove/$', views.dbinfo_remove, name='dbinfo_remove'),
    url(r'^dbinfo_change/$', views.dbinfo_change, name='dbinfo_change'),
    url(r'^db_messages/$', views.db_messages, name='db_messages'),

    url(r'^db_opera/$', views.db_opera, name='db_opera'),
    url(r'^db_query/$', views.db_query, name='db_query'),
]
