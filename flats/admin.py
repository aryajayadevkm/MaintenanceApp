from django.contrib import admin

# Register your models here.
from .models import Flat, Resident, PaymentHistory


class FlatAdmin(admin.ModelAdmin):
    list_display = ('owner', 'flat_no', 'maintenance_charge')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no', 'email')


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('flat', 'owner', 'maintenance_charge', 'amount', 'paid_for', 'remarks', 'timestamp')


admin.site.register(Flat, FlatAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)