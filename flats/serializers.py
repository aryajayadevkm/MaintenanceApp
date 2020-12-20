from rest_framework import serializers
from .models import Flat, Resident, Invoice
from jwtauth.models import Building
from .match_operations import match, match_bulk, unmatch_bulk


"""
from flats.serializers import match
f = Flat.objects.first()
bills = Bill.objects.filter(flat=f, tr_type="bill")
payments = Bill.objects.filter(flat=f, tr_type="payment")
print(match(payments, bills))
"""

ACTIONS = (('match', 'match'), ('unmatch', 'unmatch'))


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ('id', 'name', 'mobile_no', 'email')


class CreateFlatSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Flat


class InvoiceSerializer(serializers.ModelSerializer):
    flat_no = serializers.CharField(source='flat.flat_no')

    class Meta:
        model = Invoice
        fields = ('id', 'due_date', 'flat_no', 'tr_type', 'amount', 'applied', 'balance')


class FlatSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()
    building = serializers.CharField()

    class Meta:
        fields = ("building", "flat_no", "owner", "maintenance_charge", "bhk", "sq_feet", "occupants")
        model = Flat


class ViewPaymentSerializer(serializers.ModelSerializer):
    dues = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = ('id', 'flat_no', 'owner_name', 'maintenance_charge', 'dues')

    def get_dues(self, obj):
        dues = Invoice.objects.values('id', 'due_date', 'amount', 'balance', 'applied')\
            .filter(flat=obj, tr_type="bill", balance__lt=0)
        return dues


class MakePaymentSerializer(serializers.Serializer):
    amount = serializers.CharField(write_only=True)
    bill_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    remarks = serializers.CharField(allow_blank=True, required=False, write_only=True)

    def update(self, instance, validated_data):
        amount = int(validated_data.get('amount', 0))
        if amount > 0:
            Invoice.objects.create(flat=instance, tr_type="payment", amount=amount, applied=0, balance=amount)
        total_payments = Invoice.objects.filter(flat=instance, tr_type="payment", balance__gt=0)
        bill_ids = validated_data.get('bill_ids', [])
        bills = Invoice.objects.filter(id__in=bill_ids)
        matched = match(total_payments, bills)
        print(matched)
        return instance


class MatchBillSerializer(serializers.Serializer):
    flat_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.ChoiceField(choices=ACTIONS)

    def create(self, validated_data):
        ids = validated_data.get('flat_ids', [])
        print(ids)
        flats = Flat.objects.filter(pk__in=ids)
        action = validated_data.get('action', None)
        for flat in flats:
            if action == "match":
                match_bulk(flat)
            elif action == "unmatch":
                unmatch_bulk(flat)
        return flats
