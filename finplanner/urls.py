from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.login, name='login'),
    path('', views.index, name='index'),
    path('accounts/login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user/(?P<username>\w+)', views.profile, name='profile'),
    path('accounts/edit', views.edit_profile, name='edit_profile'),

]
