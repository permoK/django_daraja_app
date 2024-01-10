from django.shortcuts import render
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from .forms import StkpushForm, loginForm, CreateUserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import UserProfile, Wallet, User

import requests
import json
import base64
from datetime import datetime
import time
import re

cl = MpesaClient()
token = cl.access_token()

# Create your views here.
@login_required(login_url='login')
def home(request):
    message = messages.get_messages(request)
    user_profile = UserProfile.objects.get(username=request.user.username)

    return render(request, "home.html", {'message':message, "user_profile":user_profile})



def auth_token(request):
    context = { 'token': token }
    return render(request, "auth_token.html", context)

@login_required(login_url='login')
def payment(request):

    def stk(phone, amount):

        # Define the URL of the API endpoint
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        # timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_shortcode = "174379"
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

        # Define the data to send
        data =  {
        "BusinessShortCode": business_shortcode,
        "Password": base64.b64encode(bytes(str(business_shortcode) + str(passkey) + str(timestamp), 'utf-8')).decode('utf-8'),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone, 
        "PartyB": business_shortcode,
        "PhoneNumber": phone, 
        "CallBackURL": "https://api.darajambili.com",
        "AccountReference": "perminus K Limited🔨",
        "TransactionDesc": "Lipa Deni😂" 
    }

        # Convert the data to JSON format
        json_data = json.dumps(data)


        # Create a headers dictionary with the content type, length, and authorization
        headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json_data)),
        "Authorization": "Bearer " + token
        }

        # Send the request using requests.post and store the response
        response = requests.post(url, data=json_data, headers=headers)
        return response, response.json(), amount
        

    if request.method == 'POST':
        form = StkpushForm(request.POST)
        if form.is_valid():
            Phone_number = form.cleaned_data['phone_number']
            Amount = form.cleaned_data['amount']
            if Phone_number is not None and Amount is not None:
                stk = stk(phone = Phone_number, amount = Amount)
           
                context = { "status_code": stk[0].status_code, "successMessage": f"stk push sent successfully to pay Ksh.{Amount}",  "form":form }
                if stk[0].status_code == 200:
                    return redirect('home')
    else:
        form = StkpushForm()
        context = { "form":form }

    return render(request, "payment.html", context)


def login_view(request):
    
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home page
                messages.success(request, 'log in success.') 
                next_url = request.GET.get('next', 'home')  # 'home' is the default redirect URL
                return redirect(next_url)
            else:
                # Invalid login
                messages.error(request, 'Invalid username or password.')   
    message = messages.get_messages(request)
    return render(request, 'login.html', {'form': form,'message':message})
        
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')
   
def register(request):
    form = CreateUserForm()
    profile_form = UserProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Account was created successfully')
            return redirect('login')
    else:
        # form error
        form = CreateUserForm()
        profile_form = UserProfileForm()
        context = { "form":form, "profile_form":profile_form }
    context = { "form":form, "profile_form":profile_form, "errors":form.errors, "errors":profile_form.errors }
    return render(request, "register.html", context)



# ajax views
def check_balance(request):
    money = 100
    amount = request.POST.get('amount')
    if amount is not None and amount != '':
        if int(amount) < 0:
            return HttpResponse(f"<div style='color: orange;'>balance:{money}</div>")
        else:    
            money = money - int(amount)
            return HttpResponse(f"<div style='color: green;'>balance:{money}</div>")
    else:
        return HttpResponse(f"<div style='color: orange;'>balance:{money}</div>")

@require_http_methods(["POST"])
def check_username(request):
    username = request.POST.get('username', None)

    if username is not None and username != '':
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("<div style='color:red;'>Username already exists</div>")
        else:
            return HttpResponse("<div style='color:green;'>Username is available</div>")
    else:
        return HttpResponse("<div style='color:orange;'>Enter a username to continue</div>")


def auth_login(request):
    return HttpResponse("<div style='color: red;'>invalid username or password </div>")
    

def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        # check if email format is valid
        #
        # Regular expression for a simple email format validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return HttpResponse("<div style='color: green;'>valid email format </div>")
        else:
            return HttpResponse("<div style='color: red;'>invalid email format </div>")
    return HttpResponse("")

def check_admission_number(request):
    if request.method == 'POST':
        admission_number = request.POST.get('admission_number', None)
        # if admission number is not empty
        if admission_number is not None and admission_number != '':
            #check if admission number exists
            if get_user_model().objects.filter(admission_number=admission_number).exists():
                return HttpResponse("<div style='color: red;'>admission number already exists</div>")
            else:
                return HttpResponse("<div style='color: green;'>admission number is available</div>")
        else:
            return HttpResponse("<div style='color: orange;'>Enter an admission number to continue</div>")

def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', None)
        # if phone number is not empty
        if phone_number is not None and phone_number != '':
            # Check if the phone number starts with '254'
            # check if phone number format is valid
            phone_regex = r'^\+?1?\d{9,15}$'

            if phone_number.startswith('254') and re.match(phone_regex, phone_number):

            # Regular expression for a simple phone number format validation
                           
                return HttpResponse("<div style='color: green;'>valid phone number format </div>")
            else:
                return HttpResponse("<div style='color: red;'>phone number must start with 254 and must be valid </div>")
        else:
            return HttpResponse("<div style='color: orange;'>Enter a phone number to continue</div>")


    return HttpResponse("phone number")

def check_password1(request):
    return HttpResponse("password1")


def check_password(request):
    return HttpResponse("password")


