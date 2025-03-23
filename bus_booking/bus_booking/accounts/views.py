from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def home(request):
    return render(request, "accounts/home.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_type = request.POST.get("user_type", "passenger")  # Default to passenger

        user = CustomUser.objects.create_user(username=username, password=password, user_type=user_type)
        
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect("login")

    return render(request, "accounts/register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    # Check if the user is a superadmin (superuser in Django)
    if request.user.is_superuser:
        return redirect("/admin")  # Redirect to the superadmin dashboard

    # Check if the user is a regular admin
    elif request.user.user_type == "admin":
        return redirect("admin_dashboard")  # Redirect to the admin dashboard
    
    # For other users (passengers), redirect to the passenger dashboard
    return redirect("passenger_dashboard")  # Redirect to the passenger dashboard

    
@login_required
def passenger_dashboard(request):
    return render(request, "accounts/passenger_dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")

