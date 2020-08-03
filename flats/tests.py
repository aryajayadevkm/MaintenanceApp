from django.test import TestCase
from flats.serializers import *
from .models import *
# Create your tests here.
u = User.objects.all()
f = Flat.objects.all()
ph = PaymentHistory.objects.first()
serialized = MonthlyCollectionSerializer(ph)
print(serialized.data)