from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    BANKS = (
        ('Standard Chartered', 'Standard Chartered'),
        ('KCB', 'KCB'),
        ('Equity', 'EQUITY'),
    )

    # bio = models.CharField(max_length=60,blank=True)
    # user = models.ForeignKey(User, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",primary_key=True)
    contact = models.CharField(max_length=60,blank=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

    timestamp = models.DateTimeField(default=timezone.now,blank=True)
    bank = models.CharField(max_length=100, choices=BANKS,default="")   # timestamp = models.DateTimeField(auto_now_add=True,null = True)

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
