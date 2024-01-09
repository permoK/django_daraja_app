from django.db import models
import uuid


# Create your models here.

class MpesaPayment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1)
    phone_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    #account_reference = models.CharField(max_length=12)
    #transaction_description = models.CharField(max_length=12)
    pass
    
   

class User(models.Model):
    user_id = uuid.uuid4()
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    email = models.EmailField()
    phone_number = models.IntegerField()
    pass

    def __str__(self):
        return self.username, self.phone_number

