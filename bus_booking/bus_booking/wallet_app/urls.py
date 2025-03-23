from django.urls import path
from .views import wallet_view, add_money

urlpatterns = [
    path("", wallet_view, name="wallet_view"),  # This will be accessed as "wallet/"
    path("add/", add_money, name="add_money"),  # This will be accessed as "wallet/add/"
]
