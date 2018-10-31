from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User


# Create your views here.
def index(request):


    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        print('SUBMIT')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"That username is taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"That email is taken")
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,email=email,password=password2,first_name=first_name,last_name=last_name)
                    user.save()
                    messages.success(request,"You are now registered and can log in")
                    return redirect('login')
    else:
        return render(request,'registration/register.html')
def login(request):
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request,user)
                messages.success(request,"You are now logged in")
                return redirect('dashboard')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('login')


            print('SUBMIT')
            # return redirect('register')
        else:
            return render(request,'registration/login.html')
def dashboard(request):

    return render(request,'register/dashboard.html')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')
