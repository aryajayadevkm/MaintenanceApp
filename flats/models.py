from django.db import models

# Create your models here.
from jwtauth.models import Building


class Resident(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    mobile_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        self.name = self.name
        return self.name


class Flat(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE, blank=True, null=True)
    flat_no = models.CharField(max_length=200, null=True, blank=True)
    maintenance_charge = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.flat_no

    @property
    def building_name(self):
        return self.building.name

    @property
    def owner_name(self):
        return self.owner.name


# class PaymentHistory(models.Model):
#     flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
#     amount_paid = models.IntegerField(null=True, blank=True, default=0)
#     due_date = models.DateField(null=True, blank=True)
#     remarks = models.TextField(null=True, blank=True, max_length=200)
#     timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)
#
#     @property
#     def owner(self):
#         return self.flat.owner.name
#
#     @property
#     def maintenance_charge(self):
#         return self.flat.maintenance_charge


class Invoice(models.Model):
    TR_CHOICES = (('bill', 'bill'), ('payment', 'payment'))
    due_date = models.DateField(blank=True, null=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='bills')
    tr_type = models.CharField(max_length=20, choices=TR_CHOICES, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    applied = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


