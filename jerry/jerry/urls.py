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
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'proc/cpuinfo/$', views.cpuinfo, name='cpuinfo'),
    url(r'proc/ansiblecheck/$', views.ansiblecheck, name='ansiblecheck'),

    url(r'^cmdb/', include('cmdb.urls',namespace="cmdb")),
    url(r'^disconf/', include('disconf.urls',namespace="disconf")),
    url(r'^opera/', include('opera.urls',namespace="opera")),
    url(r'^roleget/$', views.perm_role_get, name='role_get'),
    url(r'^terminal/$', views.web_terminal, name='terminal'),
]
