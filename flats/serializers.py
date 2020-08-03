from rest_framework import serializers
from .models import Flat, Resident, PaymentHistory


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("flat_no", "owner")
        model = Flat


class ResidentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    flats = serializers.StringRelatedField(many=True)
    email_id = serializers.CharField()

    class Meta:
        model = Resident
        fields = ('username', 'mobile_no', 'email_id', 'flats')
        read_only_fields = ('username', 'email_id')


class MonthlyCollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()

    class Meta:
        model = PaymentHistory
        fields = ('flat', 'owner', 'maintenance_charge', 'amount', 'paid_for', 'remarks')
        read_only_fields = ('maintenance_charge', )

    # flat
    # amount
    # paid_for
    # remarks
