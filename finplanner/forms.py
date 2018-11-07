from django import forms
from finplanner.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.forms import ModelForm

# USER PROFILES
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','timestamp']

# EXPENSES
class ExpenseTableHelper(FormHelper):
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    form_method = 'GET'
    layout = Layout(
        Field('date', placeholder='YYYY-MM-DD'),
        Field('description'),
        Field('type'),
        Field('payment'),
        Field('amount'),
        Submit('submit', 'Filter'),
    )

class DateInput(forms.DateInput):
    input_type = 'date'

class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = [
            'date',
            'description',
            'type',
            'payment',
            'amount'
        ]
        widgets = {
            'date': DateInput(),
        }

# class ExpenseForm(forms.Form):
#     title = forms.CharField()
#     amount = forms.IntegerField()
#     category = forms.CharField()
#
# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         exclude = ['bank','user']
