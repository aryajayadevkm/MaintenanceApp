from django.db import models

# Create your models here.
from jwtauth.models import Building


class Resident(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    mobile_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Flat(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE, blank=True, null=True)
    flat_no = models.CharField(max_length=200, null=True, blank=True)
    maintenance_charge = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, default=0)
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.flat_no

    @property
    def building_name(self):
        return self.building.name

    @property
    def owner_name(self):
        return self.owner.name


class PaymentHistory(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(null=True, blank=True, default=0)
    paid_for = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def owner(self):
        return self.flat.owner.name

    @property
    def maintenance_charge(self):
        return self.flat.maintenance_charge

