#urls imports
from django.urls import path
from . import views

urlpatterns = [
        path('payment/', views.payment, name='payment'),
        path('auth_token/', views.auth_token, name='auth_token'),
        path('register/', views.register, name='register'),
        path('login/', views.login, name='login'),
        # path('logout/', views.logout, name='logout'),
        path('', views.home, name='home'),

        ]

htmx_urlpatterns = [
        path('check_balance/', views.check_balance, name='check_balance'),
        ]

urlpatterns += htmx_urlpatterns
