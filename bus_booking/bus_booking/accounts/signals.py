from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from wallet_app.models import Wallet  # Import from correct app

User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)  # Automatically creates a wallet for new users
