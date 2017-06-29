from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import  PasswordChangeForm

import json

# Create your views here.



@login_required
def index(request):
    print(request)
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
        else:
            return render(request,'login.html')
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



def test(request):
    return render(request, 'test.html')
