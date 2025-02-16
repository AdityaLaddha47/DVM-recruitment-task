from django.urls import path
from .views import register, user_login, user_logout, dashboard, logout_view, home, admin_dashboard, wallet_view, add_money
from . import views
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),  # Homepage route
    path("passenger-dashboard/", views.passenger_dashboard, name="passenger_dashboard"),
    path("", views.home, name="home"),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path("wallet/", wallet_view, name="wallet_view"),
    path("wallet/add/", add_money, name="add_money"),
]
