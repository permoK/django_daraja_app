from django.contrib import admin

# Register your models here.

from .models import MpesaPayment, User

admin.site.register(MpesaPayment)
admin.site.register(User)

