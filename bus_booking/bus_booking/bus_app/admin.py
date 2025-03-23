from django.contrib import admin
from .models import Route, Bus, Booking  # Import bus-related models

admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Booking)
