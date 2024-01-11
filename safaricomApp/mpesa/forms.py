from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Wallet

class CreateUserForm(UserCreationForm):
    email = forms.CharField(required=True, max_length=254)
    username = forms.CharField(required=True, max_length=254)

    class Meta:
        model = User 
        fields = ["username".lower(), "email","password1", "password2"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['registration_number', 'email', 'phone_number','username']


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['amount_paid', 'balance','username']

class StkpushForm(forms.Form):
    # phone_number must start with 254 and be 12 digits long
    phone_number = forms.CharField(max_length=12)
    amount = forms.IntegerField()
    # account_reference = forms.CharField(max_length=12)
    # transaction_description = forms.CharField(max_length=12)

    class Meta:
        fields = ["phone_number", "amount"]

    pass

class loginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12, widget=forms.PasswordInput())
    
    class Meta:
        fields = ["username", "password"]


