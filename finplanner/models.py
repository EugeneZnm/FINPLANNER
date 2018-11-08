from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Bank(models.Model):

    bank = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.bank
    def create_bank(self):
        self.save()
    def delete_bank(self):
        self.delete()
    @classmethod
    def find_bank(cls,search_term):
        bank = cls.objects.filter(name__icontains = search_term)
class Account(models.Model):
    name = models.CharField(max_length=100)
    budget = models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="accounts")

    def budget_left(self):
        expense_list = Expense.objects.filter(account = self)
        total_expense = 0
        for expense in expense_list:
            total_expense += expense.amount
        return self.budget - total_expense

    def total_transactions(self):
        budget_list = Account.objects.filter(budget=self)
        total_budgets = 0
        for budget in budget_list:
            total_budgets += budget.budget
        return self.budget + total_budgets

    def __str__(self):
        return self.name

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",primary_key=True)
    contact = models.CharField(max_length=60,blank=True)

    timestamp = models.DateTimeField(default=timezone.now,blank=True)



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
    @classmethod
    def get_profile(cls,id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls,id):
        profile = Profile.objects.filter(user = id).first()
        return profile
    #
    # @classmethod
    # def filter_by_id(cls, id):
    #     profile = Profile.objects.filter(user = id).first()
    #     return profile
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile
class Expense(models.Model):
    CATEGORY = (
        ("Accomodation", "Accomodation"),
        ("Food", "Food"),
        ("Groceries", "Groceries"),
        ("Transportation", "Transportation"),
        ("Entertainment", "Entertainment"),
        )

    date = models.DateField()
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=30)
    category = models.CharField(choices=CATEGORY,default="",blank=False,max_length=80)
    payment = models.CharField(max_length=30)
    amount = models.FloatField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateField()
    account=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True,related_name="expenses")


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('finplanner:expenses')
