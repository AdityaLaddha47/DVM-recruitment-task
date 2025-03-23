from django.contrib import admin
from django.urls import path, include
from .views import home
urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin panel
    path("", include("accounts.urls")),  # Routes for authentication and dashboards
    path("buses/", include("bus_app.urls")),  # Routes for bus-related functionalities
    path("wallet/", include("wallet_app.urls")),  # Routes for wallet management
    path("", home, name="home"),
]
