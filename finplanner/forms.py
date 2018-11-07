from django import forms
from finplanner.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','timestamp']

class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()
# 
# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         exclude = ['bank','user']
