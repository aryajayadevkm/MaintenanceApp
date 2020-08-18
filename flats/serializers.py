from rest_framework import serializers

from jwtauth.serializers import UserSerializer
from .models import Flat, Resident, PaymentHistory


class ResidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resident
        fields = ('name', 'mobile_no', 'email')


class FlatSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()

    class Meta:
        fields = ("building", "flat_no", "owner", "last_paid")
        model = Flat

    def update(self, instance, validated_data):
        owner = validated_data.pop('owner', None)
        for key, val in validated_data.items():
            setattr(instance, key, val)
        if owner is not None:
            instance.owner = Resident.objects.get(pk=owner)
        instance.save()
        return instance


class MonthlyCollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()
    flat = serializers.CharField()

    class Meta:
        model = PaymentHistory
        fields = ('flat', 'owner', 'maintenance_charge', 'amount', 'paid_for', 'remarks')
        read_only_fields = ('maintenance_charge', )

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        data = validated_data.get('paid_for', instance.paid_for)
        flat_serializer = FlatSerializer(instance.flat, data={"last_paid": data}, partial=True)
        flat_serializer.is_valid(raise_exception=True)
        flat_serializer.save()
        return instance


