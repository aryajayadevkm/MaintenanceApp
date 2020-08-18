from django.db import models

# Create your models here.
from jwtauth.models import User, Building


class Resident(models.Model):
    name = models.CharField(null=True, max_length=100)
    mobile_no = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Flat(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE, blank=True, null=True)
    flat_no = models.CharField(max_length=200, null=True)
    maintenance_charge = models.IntegerField(null=True)
    last_paid = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

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
        return self.flat.owner.name

    @property
    def maintenance_charge(self):
        return self.flat.maintenance_charge
