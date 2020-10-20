from rest_framework import serializers
from django.db.models import F
from .models import Flat, Resident, PaymentHistory
from jwtauth.models import Building


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


class BillSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    flat_no = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    due = serializers.IntegerField()
    amount_paid = serializers.IntegerField()
    due_date = serializers.DateField()

    def get_flat_no(self, obj):
        return obj.flat.flat_no

    def get_amount(self, obj):
        amount = obj.flat.maintenance_charge
        return amount


class DisplayCollectionSerializer(serializers.ModelSerializer):
    due_details = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = ('id', 'flat_no', 'owner_name', 'maintenance_charge', 'surplus', 'due_details')

    def get_due_details(self, obj):
        months_dues = PaymentHistory.objects.values('due_date', 'amount_paid') \
            .filter(flat=obj, amount_paid__lt=obj.maintenance_charge)\
            .annotate(due=obj.maintenance_charge - F('amount_paid'))
        return months_dues


class MakePaymentSerializer(serializers.Serializer):
    months = serializers.ListField(child=serializers.DateField(format='%Y-%m-%d'), write_only=True)
    amount_paid = serializers.CharField(write_only=True)
    remarks = serializers.CharField(write_only=True)

    # water tank analogy
    def update(self, instance, validated_data):
        if instance.surplus is None:
            instance.surplus = 0
        money = int(validated_data.get('amount_paid', 0)) + instance.surplus
        instance.surplus = 0
        dates = sorted(validated_data.get('months', []))
        for date in dates:
            try:
                record = PaymentHistory.objects.get(flat=instance,
                                                    due_date__month=date.month,
                                                    due_date__year=date.year)
            except PaymentHistory.DoesNotExist:
                record = PaymentHistory.objects.create(flat=instance, due_date=date)

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
        instance.surplus = money
        instance.save()
        return instance


