from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

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
            return HttpResponseRedirect('/')
        else:
            return render(request,'login.html')
        
            
    return render(request,'login.html')
    


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')



def test(request):
    return render(request, 'test.html')
