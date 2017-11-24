# coding: utf-8
from django.shortcuts import render,render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import  PasswordChangeForm

from cmdb.models import Asset
import subprocess


import json
import random

# Create your views here.



@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form':form})


@login_required
def cpuinfo(request):
    mess=open("/proc/loadavg","r").readline().split()[:3]
    msg = json.dumps(mess,sort_keys=True,indent=4)
    return HttpResponse(msg)

def ansiblecheck(request):
    host_list = Asset.objects.filter(is_active=True)
    success,failed=0,0
    success_ip,failed_ip = [],[]
    host_info_ips = [ host_info.ip for host_info in host_list ]
    host_info_ips = list(set(host_info_ips))
    
    ansible_check_script = 'ansible %s -m ping -f4' % ','.join(host_info_ips)
    script_info = subprocess.Popen(ansible_check_script,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    info = script_info.stdout.readlines()
    for l in info:
        if 'SUCCESS' in l:
            success += 1
            success_ip.append(l.split()[0])
        if 'UNREACHABLE' in l:
            failed += 1
            failed_ip.append(l.split()[0])

    unknown = len(host_info_ips) - success - failed
    unknown_ips = [ {'name': ip,'status':'Unknown' } for ip in host_info_ips if ip not in success_ip and ip not in failed_ip ]
    
    data_number = [success,failed,unknown]
    data_ip = unknown_ips + [ {'name': ip,'status':'Failed' } for ip in failed_ip ] + [ {'name': ip,'status':'Success' } for ip in success_ip ]
    
    data = [data_ip,data_number]
    msg = json.dumps(data,sort_keys=True,indent=4)
    return HttpResponse(msg)


def test(request):
    return render(request, 'test.html')

@login_required
def perm_role_get(request):
    asset_id = request.GET.get('id', 0)
    if asset_id:
        #asset = get_object(Asset, id=asset_id)
        asset = 1
        if asset:
            #role = user_have_perm(request.user, asset=asset)
            #logger.debug(u'获取授权系统用户: ' + ','.join([i.name for i in role]))
            #return HttpResponse(','.join([i.name for i in role]))
            return HttpResponse('iwjw')
    else:
        roles = get_group_user_perm(request.user).get('role').keys()
        return HttpResponse(','.join(i.name for i in roles))

    return HttpResponse('error')

@csrf_exempt
@login_required
def web_terminal(request):
    asset_id = request.GET.get('id')
    asset_ip = Asset.objects.get(id=asset_id).ip
    hostname = Asset.objects.get(id=asset_id).hostname
    print(asset_ip,asset_id)
    return render_to_response('web_terminal.html', locals())
