from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import timedelta
import json
from .models import Bus, Booking, Wallet

@login_required
def get_available_seats(request, bus_id):
    """Returns the available seat count for a given bus."""
    bus = get_object_or_404(Bus, id=bus_id)
    return JsonResponse({"available_seats": bus.available_seats})

@csrf_exempt
@login_required
def book_ticket(request):
    """Handles ticket booking for a user."""
    if request.method == "POST":
        data = json.loads(request.body)
        bus_id = data.get("bus_id")
        seat_count = data.get("seat_count")

        bus = get_object_or_404(Bus, id=bus_id)
        
        # Check if there are enough available seats
        if bus.available_seats < seat_count:
            return JsonResponse({"error": "Not enough seats available"}, status=400)

        # Check if the user has enough balance
        total_cost = seat_count * bus.fare
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        
        if wallet.balance < total_cost:
            return JsonResponse({"error": "Insufficient wallet balance"}, status=400)

        # Deduct balance & update seats
        wallet.balance -= total_cost
        wallet.save()

        bus.available_seats -= seat_count
        bus.save()

        # Create the booking
        booking = Booking.objects.create(user=request.user, bus=bus, seat_count=seat_count)
        return JsonResponse({"message": "Booking successful", "booking_id": booking.id})

@login_required
def cancel_booking(request, booking_id):
    """Cancels a booking, refunds the wallet, and updates available seats."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.is_cancelled:
        return JsonResponse({"error": "Booking already cancelled"}, status=400)

    # Check cancellation window (6 hours before departure)
    if booking.bus.departure_time - now() < timedelta(hours=6):
        return JsonResponse({"error": "Cancellation not allowed within 6 hours of departure"}, status=400)

    # Free up seats
    booking.bus.available_seats += booking.seat_count
    booking.bus.save()

    # Refund to wallet
    wallet = Wallet.objects.get(user=request.user)
    refund_amount = booking.seat_count * booking.bus.fare
    wallet.balance += refund_amount
    wallet.save()

    # Mark booking as cancelled
    booking.is_cancelled = True
    booking.save()
    
    return JsonResponse({"message": "Booking cancelled successfully and amount refunded."})

def bus_list(request):
    return JsonResponse({"message": "Bus list endpoint"})

from django.shortcuts import render


