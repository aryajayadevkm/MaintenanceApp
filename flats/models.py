from django.db import models

# Create your models here.
from jwtauth.models import User


class Resident(models.Model):
    # There is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile_no = models.IntegerField(null=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # flat = models.(Note, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email


class Flat(models.Model):
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='flats', blank=True, null=True)
    flat_no = models.CharField(max_length=200)
    maintenance_charge = models.IntegerField(null=True)

    def __str__(self):
        return self.flat_no


class PaymentHistory(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    paid_for = models.DateTimeField(null=True)
    remarks = models.TextField(null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def owner(self):
        return self.flat.owner.user.username

    @property
    def maintenance_charge(self):
        return self.flat.maintenance_charge
