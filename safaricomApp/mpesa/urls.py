#urls imports
from django.urls import path
from . import views

urlpatterns = [
        path('stkpush/', views.stkpush, name='stkpush'),
        path('auth_token/', views.auth_token, name='auth_token'),
        ]
