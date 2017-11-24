from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from cmdb.models import Asset
# Create your views here.

import time
import commands


def ansible_file(request):
    return render(request, 'test.html')

@csrf_exempt
@login_required
def ansible_run(request):
    if request.method == 'GET':
        hosts =  [ host_info.ip for host_info in Asset.objects.filter(is_active=True) ]
        #hosts=['10.7.253.113','10.7.253.114','10.7.253.115']
        modules = ['copy','file','cron','group','user','yum','service','script','ping','command','raw','get_url','synchronize']
        return render(request, 'disconf/ansiblerun.html', locals())
    else:
        print(request.POST)
        hostlist = request.POST.get('hostlist','')
        module = request.POST.get('module','')
        ansiblescript = request.POST.get('ansiblescript','')
        hosts = hostlist.strip().replace(' ',',')
        ansible_run = '/usr/local/bin/ansible %s -m %s -a "%s" --forks 3' %(hosts, module, ansiblescript)
        print(ansible_run)
        status,info = commands.getstatusoutput(ansible_run)
        print(status,info)
        return HttpResponse(info)


@login_required
def ansible_job_run(request):
    return render(request, 'disconf/ansiblejobrun.html', locals())

@csrf_exempt
@login_required
def ansible_job_add(request):
    if request.method == 'GET':
        jobtypes = ['run','status','run']
        playbooks = ['main.yml','iptable.yml','init.yml']
        return render(request, 'disconf/ansiblejobadd.html', locals())
    else:
        print(request.POST)
        jobname = request.POST.get('jobname','')
        project = request.POST.get('project','')
        playbook = request.POST.get('playbook','')
        forks = request.POST.get('forks','')
        jobtype = request.POST.get('jobtype','')
        inventory = request.POST.get('inventory','')
        print(forks)
        return HttpResponse('sss')

