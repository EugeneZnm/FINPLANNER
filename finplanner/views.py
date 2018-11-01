from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from finplanner.models import *
from finplanner.forms import *


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):

    message = "Hello World"

    context ={"message":message}

    return render(request,'index.html',context)
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'registration/registration.html', {'form': form})

def dashboard(request):

    return render(request,'register/dashboard.html')

@login_required(login_url='/login/')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('login')
@login_required(login_url='/login/')
def index(request):

    return render(request,'index.html')
