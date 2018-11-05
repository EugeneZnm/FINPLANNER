from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify

# Create your models here.
class Bank(models.Model):
    BANKS = (
        ('Standard Chartered', 'Standard Chartered'),
        ('KCB', 'KCB'),
        ('Equity', 'EQUITY'),
    )
    bank = models.CharField(max_length=100, choices=BANKS,default="")

    def __str__(self):
        return self.bank

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",primary_key=True)
    contact = models.CharField(max_length=60,blank=True)

    timestamp = models.DateTimeField(default=timezone.now,blank=True)
    # bank = models.ForeignKey(Bank,on_delete=models.CASCADE, null=True)


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

class Account(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,null=True,related_name="account")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Account, self).save(*args, **kwargs)
    # def save_account(self):
    #     self.save()

    def budget_left(self):
        expense_list = Expense.objects.filter(account = self)
        total_expense = 0
        for expense in expense_list:
            total_expense += expense.amount
        return self.budget - total_expense

    def __str__(self):
        return self.name

class Category(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
class Expense(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        ordering = ('-amount',)
