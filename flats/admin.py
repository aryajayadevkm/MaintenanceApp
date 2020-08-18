from django.contrib import admin

# Register your models here.
from .models import Flat, Resident, PaymentHistory, Building


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'no_of_flats')


class FlatAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'flat_no', 'maintenance_charge')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_no', 'email')


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('flat', 'owner', 'maintenance_charge', 'amount', 'paid_for', 'remarks', 'timestamp')


admin.site.register(Flat, FlatAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(Building, BuildingAdmin)