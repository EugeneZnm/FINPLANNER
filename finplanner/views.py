from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from finplanner.models import *
from finplanner.forms import SignupForm


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
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'registration/registration_form.html', {'form': form})
@login_required(login_url='/accounts/login/')
def login(request):

    return render(request, 'registration/login.html')

def dashboard(request):

    return render(request,'register/dashboard.html')

    
