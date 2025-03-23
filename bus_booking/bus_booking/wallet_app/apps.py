from django.apps import AppConfig

class WalletAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet_app"

    def ready(self):
        import wallet_app.signals  # Import signals so they are registered

class WalletAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet_app'

    def ready(self):
        import wallet_app.signals  # Import signals when the app is ready