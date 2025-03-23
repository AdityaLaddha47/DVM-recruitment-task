from django.urls import path
from .views import home, register, user_login, user_logout, dashboard, passenger_dashboard, admin_dashboard

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("passenger_dashboard/", passenger_dashboard, name="passenger_dashboard"),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
]
