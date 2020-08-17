from rest_framework import serializers

from jwtauth.serializers import UserSerializer
from .models import Flat, Resident, PaymentHistory


class FlatSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        fields = ("flat_no", "owner", "last_paid")
        model = Flat

    def get_owner(self, obj):
        return obj.owner.username


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
        user_serializer = UserSerializer(instance.user, data=validated_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return instance


class MonthlyCollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()

    class Meta:
        model = PaymentHistory
        fields = ('flat', 'owner', 'maintenance_charge', 'amount', 'paid_for', 'remarks')
        read_only_fields = ('maintenance_charge', )

    def update(self, instance, validated_data):
        data = {}
        instance.amount = validated_data.get('amount', instance.amount)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.paid_for = validated_data.get('paid_for', instance.paid_for)

        data['last_paid'] = validated_data.get('paid_for', instance.paid_for)
        flat_serializer = FlatSerializer(instance.flat, data=data, partial=True)
        flat_serializer.is_valid(raise_exception=True)
        flat_serializer.save()
        return instance


