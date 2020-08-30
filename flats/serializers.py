from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework.utils import json

from jwtauth.serializers import UserSerializer
from .models import Flat, Resident, PaymentHistory
from jwtauth.models import Building


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ('name', 'mobile_no', 'email')


class FlatSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()
    building = serializers.CharField()

    class Meta:
        fields = ("building", "flat_no", "owner", "maintenance_charge", "last_paid")
        model = Flat

    def update(self, instance, validated_data):
        print("#1", validated_data)

        owner = validated_data.pop('owner', None)
        building = validated_data.pop('building', None)
        for key, val in validated_data.items():
            setattr(instance, key, val)
        if owner is not None:
            instance.owner = Resident.objects.get(pk=owner)
        if building is not None:
            instance.building = Building.objects.get(pk=building)
        instance.save()
        return instance


"""from flats.serializers import DisplayCollectionSerializer as dcs, DateSerializer as ds"""


class DisplayCollectionSerializer(serializers.ModelSerializer):
    dues = serializers.SerializerMethodField()
    months = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = ('flat_no', 'owner_name', 'maintenance_charge', 'stock', 'dues', 'months')

    def get_dues(self, obj):
        flat = self.instance
        payment_histories_with_dues = PaymentHistory.objects.values('amount_paid') \
            .filter(flat=obj, amount_paid__lt=obj.maintenance_charge)
        dues = 0
        for payment_history in payment_histories_with_dues:
            dues += obj.maintenance_charge - payment_history['amount_paid']
        return dues

    def get_months(self, obj):
        months = PaymentHistory.objects.values_list('paid_for') \
            .filter(flat=obj, amount_paid__lt=obj.maintenance_charge)
        return [month[0] for month in months]


# from flats.serializers import MakePaymentSerializer as mps


class MakePaymentSerializer(serializers.Serializer):
    months = serializers.ListField(child=serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ'), write_only=True)
    amount_paid = serializers.CharField(write_only=True)
    remarks = serializers.CharField(write_only=True)

    # water tank analogy
    def update(self, instance, validated_data):
        if instance.stock is None:
            instance.stock = 0
        money = int(validated_data.get('amount_paid', 0)) + instance.stock
        instance.stock = 0
        dates = sorted(validated_data.get('months', []))
        for date in dates:
            try:
                record = PaymentHistory.objects.get(flat=instance,
                                                    paid_for__month=date.month,
                                                    paid_for__year=date.year)
            except PaymentHistory.DoesNotExist:
                record = PaymentHistory.objects.create(flat=instance, paid_for=date)
            record.remarks = validated_data.get('remarks', None)
            if record.amount_paid is None:
                record.amount_paid = 0
            rest_amount = instance.maintenance_charge - record.amount_paid
            if money >= rest_amount:
                record.amount_paid = instance.maintenance_charge
                money -= rest_amount
            else:
                record.amount_paid = money
                money = 0
            record.save()
        instance.stock = money
        instance.save()
        return instance


