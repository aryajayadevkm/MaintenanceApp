from rest_framework import serializers
from .models import Flat, Resident


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "flat_no","owner")
        model = Flat


class ResidentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    flats = serializers.StringRelatedField(many=True)

    class Meta:
        model = Resident
        fields = ('username', 'mobile_no', 'flats')
        read_only_fields = ('username',)

