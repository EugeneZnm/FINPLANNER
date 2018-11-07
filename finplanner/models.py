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
    date = models.DateField()
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=30)
    payment = models.CharField(max_length=30)
    amount = models.FloatField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateField()


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('finplanner:expenses')
