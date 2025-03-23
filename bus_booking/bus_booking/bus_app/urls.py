from django.urls import path
from .views import bus_list  # Import bus_list properly
from . import views
urlpatterns = [
    path("", bus_list, name="bus_list"),  # Route for bus list
    path("available_seats/<int:bus_id>/", views.get_available_seats, name="available_seats"),
    
]
