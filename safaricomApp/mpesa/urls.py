#urls imports
from django.urls import path
from . import views

urlpatterns = [
        path('payment/', views.payment, name='payment'),
        path('auth_token/', views.auth_token, name='auth_token'),
        path('register/', views.register, name='register'),
        path('login/', views.login_view, name='login'),
        path('logout_view/', views.logout_view, name='logout'),
        path('', views.home, name='home'),
        
        ]

htmx_urlpatterns = [
        path('check_balance/', views.check_balance, name='check_balance'),
        path('check_username/', views.check_username, name='check_username'),
        ]

urlpatterns += htmx_urlpatterns
