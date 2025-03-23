from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - ₹{self.balance}"

    def add_money(self, amount):
        """ Add money to the wallet """
        self.balance += amount
        self.save()

    def deduct_money(self, amount):
        """ Deduct money if sufficient balance exists """
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False  # Not enough balance

    

    