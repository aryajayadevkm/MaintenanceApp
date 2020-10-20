from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flat, PaymentHistory
from datetime import datetime


@receiver(post_save, sender=Flat)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        print("created blank payment record for", instance)
        today = datetime.today()
        PaymentHistory.objects.create(flat=instance, due_date=today.date())
