from django.db import models


# Create your models here.

class MpesaPayment(models.Model):
    phone_number = models.CharField(max_length=12)
    amount = models.IntegerField()
    account_reference = models.CharField(max_length=12)
    transaction_description = models.CharField(max_length=12)
    pass
    
    def __str__(self):
        return self.phone_number


class User(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    email = models.EmailField()
    phone_number = models.IntegerField()
    pass

    def __str__(self):
        return self.username, self.phone_number

