from django.contrib import admin

# Register your models here.
from .models import Flat, Resident, Building, Invoice


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'no_of_flats')


class FlatAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'flat_no', 'maintenance_charge', 'created')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_no', 'email')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('due_date', 'flat', 'tr_type', 'amount', 'applied', 'balance', 'created')


admin.site.register(Flat, FlatAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
