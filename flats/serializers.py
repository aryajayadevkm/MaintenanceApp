from rest_framework import serializers

from jwtauth.serializers import UserSerializer
from .models import Flat, Resident, PaymentHistory


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("flat_no", "owner")
        model = Flat


class ResidentSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    flats = serializers.StringRelatedField(many=True)
    email = serializers.CharField()

    class Meta:
        model = Resident
        fields = ('username', 'mobile_no', 'email', 'flats')
        read_only_fields = ('flats',)

    def update(self, instance, validated_data):
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        validated_data.pop('mobile_no', None)
        userserializer = UserSerializer(instance.user, data=validated_data, partial=True)
        userserializer.is_valid(raise_exception=True)
        userserializer.save()
        return instance


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
