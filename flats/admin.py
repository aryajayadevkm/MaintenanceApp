from django.contrib import admin

# Register your models here.
from .models import Flat, Resident, PaymentHistory, Building, Bill


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'no_of_flats')


class FlatAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'flat_no', 'maintenance_charge', 'surplus')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_no', 'email')


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('flat', 'owner', 'maintenance_charge', 'amount_paid', 'due_date', 'remarks', 'timestamp')


class BillAdmin(admin.ModelAdmin):
    list_display = ('date', 'flat', 'tr_type', 'amount', 'applied', 'balance')


admin.site.register(Flat, FlatAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)

admin.site.register(Bill, BillAdmin)