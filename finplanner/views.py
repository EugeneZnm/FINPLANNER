from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse, HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from finplanner.models import *
from finplanner.forms import *
from django.views.generic import CreateView
from django.utils.text import slugify
import json


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    banks=Bank.objects.all()
    context={"banks":banks}
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
    print(account_list)
    return render(request, 'account-list.html',{"account_list":account_list})

# create account view
def account_detail(request, account_slug):
    account = get_object_or_404(Account, slug=account_slug)

    # expense_list = Account.expenses.all()
    # expense_list = Expense.objects.all()


    if request.method == 'GET':
        category_list = Category.objects.filter(account=account)
        return render(request, 'account-detail.html', {'account':account,  'category_list':category_list,"expense_list":account.expenses.all()})

    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, account=account, name=category_name)

            Expense.objects.create(account=account, title=title, amount=amount, category=category).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(account_slug)


class AccountCreateView(CreateView):
    model = Account
    template_name= 'add-account.html'
    fields = ('name', 'budget',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                account=Account.objects.get(id=self.object.id),
                name=category
            ).save()

        # banks = self.request.POST['bank']
        # for bank in banks:
        #     Bank.objects.create(
        #         account=Account.objects.get(id=self.object.id),
        #         name=bank
        #     ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])

@login_required(login_url='/accounts/login/')
def new_account(request,bank_id):
    bank = get_object_or_404(Bank, pk=bank_id)
    current_user = request.user
    if request.method == 'POST':
        form = AccountForm(request.POST,request.FILES)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = current_user
            new_account.bank=bank
            assert isinstance(new_account.save, object)
            new_account.save()
            return redirect('index')
    else:
        form = AccountForm()
        # context= {"form":form}
    return render(request, 'add-account.html',{"form":form})
