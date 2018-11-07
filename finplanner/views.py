from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse, HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic


from finplanner.models import *
from finplanner.forms import *
# NEW
from django.views.generic import CreateView
from django.utils.text import slugify
from django.urls import reverse
from django_tables2 import RequestConfig
from django.db.models import Sum, Count
from .tables import ExpenseTable
from .filters import ExpenseFilter
from .utils import AmountUnitUtil
from django.db.models import Sum, Count
from calendar import monthrange
import json
import random
import datetime
# import django_filters

# RESTRUCTURED APP
class Dashboard():
    template_name = "tracker/dashboard.html"

    def index(request):
        # init
        avg_year = 0
        avg_month = 0
        avg_day = 0

        now = datetime.datetime.now()

        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        # count total record
        total_records = exp.count()

        # count total record in this month
        current_month = now.month
        total_records_in_this_month = exp.filter(created_at__month=current_month).count()
        if total_records_in_this_month is None:
            total_records_in_this_month = 0

        # count total record in last month
        last_month = now.month - 1
        if last_month<0:
            last_month = 11
        total_records_in_last_month = exp.filter(created_at__month=last_month).count()
        if total_records_in_last_month is None:
            total_records_in_last_month = 0

        print(total_records_in_this_month)
        print(total_records_in_last_month)
        # diff between this month and last month
        if total_records == 0:
            total_records_diff = 0
        else:
            total_records_diff = ( (total_records_in_this_month - total_records_in_last_month) / total_records ) * 100

        # sum up all the expenses
        total_expenses = exp.aggregate(amount=Sum('amount'))['amount']
        if total_expenses is None:
            total_expenses = 0

        # sum up all the expenses in this month
        total_expenses_in_this_month = exp.filter(created_at__month=current_month).aggregate(amount=Sum('amount'))['amount']
        if total_expenses_in_this_month is None:
            total_expenses_in_this_month = 0

        # sum up all the expenses in last month
        total_expenses_in_last_month = exp.filter(created_at__month=last_month).aggregate(amount=Sum('amount'))['amount']
        if total_expenses_in_last_month is None:
            total_expenses_in_last_month = 0

        # diff between this month and last month
        if total_expenses == 0:
            total_expenses_diff = 0
        else:
            total_expenses_diff = ( (total_expenses_in_this_month - total_expenses_in_last_month) / total_expenses ) * 100

        # get all categories
        categories = list(exp.values('type').distinct().order_by('type').values_list('type', flat=True))

        # get categories record count
        categories_record_cnt = list(exp.values('type').annotate(the_count=Count('type')).order_by('type').values_list('the_count', flat=True))

        # categories count
        categories_cnt = exp.values('type').annotate(the_count=Count('type')).count()
        if categories_cnt is None:
            categories_cnt = 0

        # total expense per category
        categories_expense = list(exp.values('type').order_by('type').annotate(the_count=Sum('amount')).values_list('the_count', flat=True))

        categories_color_arr = []
        for cat in categories:
            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            categories_color_arr.append(color)

        # categories count in this month
        categories_in_this_month = exp.filter(created_at__month=current_month).values('type').annotate(the_count=Count('type')).count()
        if categories_in_this_month is None:
            categories_in_this_month = 0

        # categories count in last month
        categories_in_last_month = exp.filter(created_at__month=last_month).values('type').annotate(the_count=Count('type')).count()
        if categories_in_last_month is None:
            categories_in_last_month = 0

        # diff between this month and last month
        if categories_cnt == 0:
            total_categories_diff = 0
        else:
            total_categories_diff = ((categories_in_this_month - categories_in_last_month) / categories_cnt) * 100

        # list out dates for the following processing.
        dates = list(exp.values('date')
                     .values_list('date', flat=True))

        # avg amount per year, per month and per day
        year_arr = []
        month_arr = []
        day_arr = []

        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
            if date.year not in month_arr:
                month_arr.append(date.month)
            if date.year not in day_arr:
                day_arr.append(date.day)

        if total_expenses > 0:
            avg_year = AmountUnitUtil.convertToMills(total_expenses / year_arr.__len__())
            avg_month = AmountUnitUtil.convertToMills(total_expenses / month_arr.__len__())
            avg_day = AmountUnitUtil.convertToMills(total_expenses / day_arr.__len__())
            total_expenses = AmountUnitUtil.convertToMills(total_expenses)

        # Get Latest 30 days records

        latest30DaysArr = list(exp.filter(created_at__lte=datetime.datetime.today(),
                                       created_at__gt=datetime.datetime.today() - datetime.timedelta(days=30))
                            .values('date').distinct().order_by('date').values_list('date', flat=True))

        latest30DaysLabel = []
        for day in latest30DaysArr:
            latest30DaysLabel.append(day.strftime('%d/%m'))


        latest30DaysData = list(exp.filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30))
                             .values('date').distinct().order_by('date')
                             .annotate(amount=Sum('amount')).values_list('amount', flat=True))

        context = {
            'context_type': 'dashboard',
            'total_records': total_records,
            'total_expenses': total_expenses,
            'categories': categories,
            'categories_record_cnt': categories_record_cnt,
            'categories_cnt': categories_cnt,
            'categories_expense': categories_expense,
            'categories_color_arr': categories_color_arr,
            'avg_year': avg_year,
            'avg_month': avg_month,
            'avg_day':avg_day,
            'current_year': now.year,
            'current_month': now.month,
            'current_day': now.day,
            'latest30DaysLabel': latest30DaysLabel,
            'latest30DaysData': latest30DaysData,
            'totalRecordsInThisMonth': total_records_in_this_month,
            'totalRecordsInLastMonth': total_records_in_last_month,
            'totalExpensesInThisMonth': float("{0:.2f}".format(total_expenses_in_this_month)),
            'totalExpensesInLastMonth': float("{0:.2f}".format(total_expenses_in_last_month)),
            'categories_in_this_month': categories_in_this_month,
            'categories_in_last_month': categories_in_last_month,
            'total_expenses_diff': float("{0:.2f}".format(total_expenses_diff)),
            'total_records_diff': float("{0:.2f}".format(total_records_diff)),
            'total_categories_diff': float("{0:.2f}".format(total_categories_diff))

        }

        return render(request, "dashboard.html", context)

class IndexView(generic.ListView):
    template_name = "expenses.html"
    context_object_name = "records"
    model = Expense
    table_class = ExpenseTable
    filter_class = ExpenseFilter
    formhelper_class = ExpenseTableHelper

    def get_queryset(self):
        return Expense.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        filter = ExpenseFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = ExpenseTableHelper()
        table = ExpenseTable(filter.qs)
        table.order_by = '-date'
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class ExpenseCreate(CreateView):
    model = Expense
    form_class = AddExpenseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.created_at = datetime.datetime.now()
        obj.save()
        return HttpResponseRedirect(reverse_lazy('finplanner:expense'))


# # Create your views here.
# @login_required(login_url='/accounts/login/')
# def index(request):
#     banks=Bank.objects.all()
#     context={"banks":banks}
#     return render(request,'index.html',context)
# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#
#             return redirect('login')
#     else:
#         form = SignUpForm()
#
#     return render(request, 'registration/registration_form.html', {'form': form})
# @login_required(login_url='/accounts/login/')
# def login(request):
#
#     return render(request, 'registration/login.html')
#
# def dashboard(request):
#
#     return render(request,'register/dashboard.html')
#
# # PROFILE
# def profile(request, username):
#     profile = User.objects.get(username=username)
#     try:
#         profile_info = Profile.get_profile(profile.id)
#     except:
#         profile_info = Profile.filter_by_id(profile.id)
#     title= f'@{profile.username}'
#     return render(request, 'profile.html', {'title':title, 'profile':profile, 'profile_info':profile_info})
#
# def edit_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             edit = form.save(commit=False)
#             edit.user = request.user
#             edit.save()
#             return redirect('profile', username=request.user)
#
#     else:
#         form = ProfileForm()
#
#     return render(request, 'edit_profile.html', {'form':form, 'profile':profile})
#
# # END PROFILE
#
# # ACCOUNT
#
# def account_list(request,bank_id):
#     # account_list = Account.objects.all()
#     bank = get_object_or_404(Bank, pk=bank_id)
#     # bank=Bank.objects.get(id=bank_id)
#     print(bank)
#     # banks=Bank.objects.all()
#     print(account_list)
#     return render(request, 'account-list.html',{"account_list":account_list,"bank":bank})
#
# # create account view
# def account_detail(request, id):
#     account = get_object_or_404(Account, pk=id)
#
#     # expense_list = Account.expenses.all()
#     # expense_list = Expense.objects.all()
#
#
#     if request.method == 'GET':
#         category_list = Category.objects.filter(account=account)
#         return render(request, 'account-detail.html', {'account':account,  'category_list':category_list,"expense_list":account.expenses.all()})
#
#     elif request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             amount = form.cleaned_data['amount']
#             # category_name = form.cleaned_data['category']
#             #
#             # category = get_object_or_404(Category, account=account, name=category_name)
#
#             Expense.objects.create(account=account, title=title, amount=amount).save()
#
#     elif request.method == 'DELETE':
#         id = json.loads(request.body)['id']
#         expense = get_object_or_404(Expense, id=id)
#         expense.delete()
#
#         return HttpResponse('')
#
#     return HttpResponseRedirect(reverse('detail',args=(account.id,)))
#
#
#
#     def get_success_url(self):
#         return slugify(self.request.POST['name'])
#
# @login_required(login_url='/accounts/login/')
# def new_account(request,bank_id):
#     bank = get_object_or_404(Bank, pk=bank_id)
#     current_user = request.user
#     if request.method == 'POST':
#         form = AccountForm(request.POST,request.FILES)
#         if form.is_valid():
#             new_account = form.save(commit=False)
#             new_account.user = current_user
#             new_account.bank=bank
#             assert isinstance(new_account.save, object)
#             new_account.save()
#             return redirect('index')
#     else:
#         form = AccountForm()
#         # context= {"form":form}
#     return render(request, 'add-account.html',{"form":form})
