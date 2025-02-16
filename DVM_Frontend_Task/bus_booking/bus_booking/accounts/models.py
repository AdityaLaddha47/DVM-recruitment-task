from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('passenger', 'Passenger'),
        ('admin', 'Administrator'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='passenger')

    def __str__(self):
        return self.username
class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.source} → {self.destination}"

class Bus(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=20, unique=True)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    departure_time = models.DateTimeField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bus {self.bus_number} ({self.route})"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_count = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user} for {self.bus}"

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

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

    def __str__(self):
        return f"{self.user.username}'s Wallet - ₹{self.balance}"

    

