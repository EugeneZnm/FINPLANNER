from django.contrib import admin

from finplanner.models import *
# Register your models here.

admin.site.register(Profile)

admin.site.register(Expense)
admin.site.register(Bank)
admin.site.register(Account)
