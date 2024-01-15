#urls imports
from django.urls import path
from . import views

urlpatterns = [
        path('payment/fees', views.payment, name='payment'),
        path('auth_token/', views.auth_token, name='auth_token'),
        path('register/', views.register, name='register'),
        path('login/', views.login_view, name='login'),
        path('logout_view/', views.logout_view, name='logout'),
        path('', views.home, name='home'),
        path('payment/pricing', views.pricing, name='pricing'),
        
        ]

htmx_urlpatterns = [
        path('check_balance/', views.check_balance, name='check_balance'),
        path('check_username/', views.check_username, name='check_username'),
        path('check_email/', views.check_email, name='check_email'),
        path('check_password/', views.check_password, name='check_password'),
        path('check_phone_number/', views.check_phone_number, name='check_phone_number'),
        path('check_admission_number/', views.check_admission_number, name='check_admission_number'),
        path('check_password1/', views.check_password1, name='check_password1'),

        path('auth_login/', views.auth_login, name='auth_login'),
        

        

        ]

urlpatterns += htmx_urlpatterns
