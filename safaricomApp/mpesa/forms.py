from django import forms
from .models import MpesaPayment, User

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django  import forms


class CreateUserForm(UserCreationForm):
    email = forms.CharField(required=True, max_length=254)
        
    # age = forms.IntegerField(max_value=100)
    # day = forms.IntegerField(max_value=100)
    # month = forms.IntegerField(max_value=31)
    # year = forms.IntegerField(max_value=3000)
    class Meta:
        model = User 
        fields = ["username", "email", "password1", "password2"]

class StkpushForm(forms.Form):
    phone_number = forms.IntegerField()
    amount = forms.IntegerField()
    # account_reference = forms.CharField(max_length=12)
    # transaction_description = forms.CharField(max_length=12)
    pass

class loginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12)



