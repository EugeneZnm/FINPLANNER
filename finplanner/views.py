from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from finplanner.models import *
from finplanner.forms import *
from django.views.generic import CreateView
from django.utils.text import slugify


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

# PROFILE
def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    title= f'@{profile.username}'
    return render(request, 'profile.html', {'title':title, 'profile':profile, 'profile_info':profile_info})

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile', username=request.user)

    else:
        form = ProfileForm()

    return render(request, 'edit_profile.html', {'form':form, 'profile':profile})

# END PROFILE

# ACCOUNT

def account_list(request):
    account_list = Account.objects.all()
    return render(request, 'account-list.html')

# create account view
class AccountCreateView(CreateView):
    model = Account
    template_name= 'add-account.html'
    fields = ('name', 'budget')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                account=Account.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])
