from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet
from decimal import Decimal

@login_required
def wallet_view(request):
    """Display the wallet balance."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    return render(request, "wallet_app/wallet.html", {"wallet": wallet})

@login_required
def add_money(request):
    """Simulate adding money to the wallet."""
    if request.method == "POST":
        amount = request.POST.get("amount")

        if amount:
            try:
                amount = Decimal(amount)  # ✅ Directly convert to Decimal
                
                if amount > 0:
                    wallet, _ = Wallet.objects.get_or_create(user=request.user)
                    wallet.balance += amount  # ✅ Directly update balance
                    wallet.save()  # ✅ Save changes to the database
                    messages.success(request, f"₹{amount} added to your wallet!")
                else:
                    messages.error(request, "Amount must be greater than zero.")
            except Exception:
                messages.error(request, "Invalid amount entered.")

        return redirect("wallet_view")

    return render(request, "wallet_app/add_money.html")
