from django.contrib import admin

# Register your models here.

from .models import Wallet, User, UserProfile

admin.site.register(UserProfile)
admin.site.register(Wallet)
