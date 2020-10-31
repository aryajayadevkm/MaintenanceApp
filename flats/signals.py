from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flat, PaymentHistory, Bill
from datetime import datetime


@receiver(post_save, sender=Flat)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        print("created bill for", instance)
        today = datetime.today()
        PaymentHistory.objects.create(flat=instance, due_date=today.date())
        Bill.objects.create(flat=instance, tr_type="bill", amount=(-instance.maintenance_charge)
                             , applied=0, balance=(-instance.maintenance_charge))
