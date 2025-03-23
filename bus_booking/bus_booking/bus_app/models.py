from django.db import models
from django.conf import settings
from django.utils.timezone import now  
from datetime import timedelta
from wallet_app.models import Wallet  # Import from wallet_app

class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.source} → {self.destination}"

class Bus(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=20, unique=True)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(default=0)
    departure_time = models.DateTimeField(default=now)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Bus {self.bus_number} ({self.route})"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_count = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def cancel_booking(self):
        """Cancel the booking, free up seats, and refund the wallet"""
        if self.is_cancelled:
            return "Booking already cancelled."
        
        # Check if cancellation is within the allowed timeframe
        if self.bus.departure_time - now() < timedelta(hours=6):
            return "Cancellation not allowed within 6 hours of departure."

        # Free up seats
        self.bus.available_seats += self.seat_count
        self.bus.save()

        # Refund to user's wallet
        user_wallet, _ = Wallet.objects.get_or_create(user=self.user)
        refund_amount = self.seat_count * self.bus.fare
        user_wallet.balance += refund_amount
        user_wallet.save()

        # Mark as cancelled
        self.is_cancelled = True
        self.save()
        return "Booking successfully cancelled and amount refunded."

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.bus}"
