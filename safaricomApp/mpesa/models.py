from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your models here.



class UserProfile(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=12, unique=True, null=False, blank=False, default=True)
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
        return f"{self.user.username} - {self.registration_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the user already has a wallet
        if not hasattr(self, 'wallet'):
            # Create a new Wallet instance for the user
            Wallet.objects.create(user=self, username=self.username, amount_paid=0, balance=0)


class Wallet(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wallet') 
    username = models.CharField(max_length=12, unique=True, null=False, blank=False, default=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - Amount Paid: {self.amount_paid}, Balance: {self.balance}"
