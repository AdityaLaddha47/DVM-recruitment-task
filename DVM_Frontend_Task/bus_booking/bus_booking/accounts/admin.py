from django.contrib import admin
from .models import Route, Bus, Booking, Wallet

admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Wallet)

# Register your models here.
