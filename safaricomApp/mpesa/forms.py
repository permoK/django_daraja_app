from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Wallet

class CreateUserForm(UserCreationForm):
    email = forms.CharField(required=True, max_length=254)
    class Meta:
        model = User 
        fields = ["username".lower(), "email","password1", "password2"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['registration_number', 'email', 'phone_number']


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['amount_paid', 'balance']

class StkpushForm(forms.Form):
    phone_number = forms.IntegerField()
    amount = forms.IntegerField()
    # account_reference = forms.CharField(max_length=12)
    # transaction_description = forms.CharField(max_length=12)
    pass

class loginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12)
    
    class Meta:
        fields = ["username", "password"]


