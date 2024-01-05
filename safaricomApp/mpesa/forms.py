from django import forms

class StkpushForm(forms.Form):
    phone_number = forms.IntegerField()
    amount = forms.IntegerField()
    # account_reference = forms.CharField(max_length=12)
    # transaction_description = forms.CharField(max_length=12)
    pass

class loginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12)

class registerForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12)
    email = forms.EmailField()
    phone_number = forms.IntegerField()
    pass
