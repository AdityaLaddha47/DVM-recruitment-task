from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from .forms import PassengerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet
from django.db.models import F
# Create your views here.
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # Redirect to a dashboard after login
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    if request.user.is_superuser:  # ✅ Check if the user is a superuser
        return redirect("/admin/")  # 🔄 Redirect them to Django's admin panel
    
    # If user is not a superuser, check if they have a user_type field
    if hasattr(request.user, "user_type"):  
        if request.user.user_type == "admin":
            return redirect("admin_dashboard")  # Custom admin dashboard
        else:
            return redirect("passenger_dashboard")  # Passenger dashboard
    
    return redirect("login")  # Fallback redirect if something is wrong

def register(request):
    if request.method == "POST":
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect("passenger_dashboard")  # Redirect to dashboard
    else:
        form = PassengerRegistrationForm()
    
    return render(request, "accounts/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    return render(request, "accounts/home.html")  # Render homepage
@login_required
def passenger_dashboard(request):
    return render(request, "accounts/passenger_dashboard.html")

def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def wallet_view(request):
    """ Display wallet balance """
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, "wallet.html", {"wallet": wallet})

@login_required
def add_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")  # Get amount from form
        if amount:
            try:
                amount = float(amount)
                wallet, created = Wallet.objects.get_or_create(user=request.user)
                wallet.balance = F("balance") + amount  # Use F() to prevent race conditions
                wallet.save()
                messages.success(request, "Money added successfully!")
            except ValueError:
                messages.error(request, "Invalid amount entered!")
        else:
            messages.error(request, "Amount is required!")

    return redirect("wallet_home")  # Redirect to wallet page