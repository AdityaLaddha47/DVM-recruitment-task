from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Wallet

User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    """Create a wallet automatically when a new user registers."""
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    """Ensure wallet is saved when the user is saved."""
    instance.wallet.save()
