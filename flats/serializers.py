from rest_framework import serializers
from django.db.models import F, Sum
from .models import Flat, Resident, PaymentHistory, Bill
from jwtauth.models import Building


def match(payments, bills):
    i, j = 0, 0
    np, nb = len(payments), len(bills)
    while i < np and j < nb:
        balance = payments[i].balance + bills[j].balance
        (payments[i].balance, bills[j].balance) = (balance, 0) if balance >= 0 else (0, balance)
        bills[j].applied = bills[j].balance - bills[j].amount
        payments[i].applied = payments[i].balance - payments[i].amount
        bills[j].save(), payments[i].save()
        if balance >= 0:
            j += 1
        else:
            i += 1
    return [payments, bills]


def match_bulk(flat):
    payments = Bill.objects.filter(flat=flat, tr_type="payment", balance__gt=0)
    bills = Bill.objects.filter(flat=flat, tr_type="bill", balance__lt=0)
    match(payments, bills)


def unmatch_bulk(flat):
    Bill.objects.filter(flat=flat).update(balance=F('amount'), applied=0)

"""
from flats.serializers import match
f = Flat.objects.first()
bills = Bill.objects.filter(flat=f, tr_type="bill")
payments = Bill.objects.filter(flat=f, tr_type="payment")
print(match(payments, bills))
"""

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ('name', 'mobile_no', 'email')


class CreateFlatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("building", "flat_no", "owner", "maintenance_charge", "surplus")
        model = Flat


class FlatSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()
    building = serializers.CharField()

    class Meta:
        fields = ("building", "flat_no", "owner", "maintenance_charge", "surplus")
        model = Flat


class BillSerializer(serializers.ModelSerializer):
    flat_no = serializers.CharField(source='flat.flat_no')

    class Meta:
        model = Bill
        fields = ('id', 'date', 'flat_no', 'tr_type', 'amount', 'applied', 'balance')


class ViewPaymentSerializer(serializers.ModelSerializer):
    dues = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = ('id', 'flat_no', 'owner_name', 'maintenance_charge', 'dues')

    def get_dues(self, obj):
        dues = Bill.objects.values('id', 'date', 'amount', 'balance').filter(flat=obj, tr_type="bill", balance__lt=0)
        return dues


class MakePaymentSerializer(serializers.Serializer):
    amount = serializers.CharField()
    bill_ids = serializers.ListField(child=serializers.IntegerField())
    remarks = serializers.CharField()

    def update(self, instance, validated_data):
        amount = validated_data.get('amount', 0)
        if amount > 0:
            Bill.objects.create(flat=instance, tr_type="payment", amount=amount, applied=0, balance=amount)
        total_payments = Bill.objects.filter(flat=instance, tr_type="payment", balance__gt=0)
        bill_ids = validated_data.get('bill_ids', [])
        bills = Bill.objects.filter(id__in=bill_ids)
        matched = match(total_payments, bills)
        print(matched)
        return instance
