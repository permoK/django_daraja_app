from django.shortcuts import render
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from .forms import StkpushForm, loginForm, CreateUserForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

import requests
import json
import base64
from datetime import datetime
import time

cl = MpesaClient()
token = cl.access_token()

# Create your views here.
def home(request):
    return render(request, "home.html")



def auth_token(request):
    context = { 'token': token }
    return render(request, "auth_token.html", context)


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
    else:
        form = StkpushForm()
        context = { "form":form }

    return render(request, "payment.html", context)

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


def login(request):
    form = loginForm()
    context = { "form":form }
    return render(request, "login.html", context)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
           form.save()
    else:
        form = CreateUserForm()
        context = { "form":form }
    context = { "form":form }
    return render(request, "register.html", context)


