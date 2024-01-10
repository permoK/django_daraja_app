from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your models here.



class UserProfile(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    registration_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False, default=True)
    phone_number = models.CharField(max_length=15)
    
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="user_profiles",
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="user_profiles",
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username
    
    def __str__(self):
        return f"{self.user.username} - {self.registration_number}"

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - Amount Paid: {self.amount_paid}, Balance: {self.balance}"
