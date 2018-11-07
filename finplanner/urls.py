from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # RESTRUCTURED VIEWS
    path('', views.LandingView.landing, name ="landing"),

    path('dashboard', login_required(views.Dashboard.index), name="dashboard"),
    path('expense/add', login_required(views.ExpenseCreate.as_view()), name="create_expense"),
    path('expenses', login_required(views.IndexView.as_view()), name ="expenses"),




    # # path('', views.login, name='login'),
    # path('', views.index, name='index'),
    # path('accounts/login/', views.login, name='login'),
    # path('register', views.register, name='register'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('user/(?P<username>\w+)', views.profile, name='profile'),
    # path('accounts/edit', views.edit_profile, name='edit_profile'),
    # path('list/(?P<bank_id>\d+)', views.account_list, name="list"),
    # # path('add', views.AccountCreateView.as_view(), name="add"),
    # path('account/(?P<id>\d+)', views.account_detail, name="detail"),
    #
    # path('new_account/(?P<bank_id>\d+)', views.new_account, name='new_account'),


]
