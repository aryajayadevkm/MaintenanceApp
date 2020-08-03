from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from .models import Flat, Resident, PaymentHistory
from .serializers import FlatSerializer, ResidentSerializer, MonthlyCollectionSerializer
from rest_framework.exceptions import PermissionDenied


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class FlatListViewSet(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer

    def get(self, request):
        flat_list = Flat.objects.all()
        serializer = self.serializer_class(flat_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'post failed'})


class ResidentListViewSet(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        resident_list = Resident.objects.all()
        serializer = ResidentSerializer(resident_list, many=True)
        return Response(serializer.data)


"""
data looks like {"flat" :"1", "amount" :"1200", "paid_for" :, "remarks":"nil"}
"""
class MonthlyCollectionViewSet(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MonthlyCollectionSerializer

    def get(self, request):
        collection_list = PaymentHistory.objects.all()
        serializer = self.serializer_class(collection_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'post failed'})


class MonthlyCollectionListCreateView(ListCreateAPIView):
    serializer_class = MonthlyCollectionSerializer

    def get_queryset(self):
        today = datetime.today()
        flats_already_paid_this_month = PaymentHistory.objects.filter(paid_for__month=today.month, paid_for__year=today.year)\
            .values_list('flat', flat=True)
        remaining_flats = Flat.objects.exclude(id__in=flats_already_paid_this_month)
        for flat in remaining_flats:
            blank_payment_record = PaymentHistory.objects.create(flat=flat)
            print(blank_payment_record)
        return PaymentHistory.objects.filter(paid_for=None)|PaymentHistory.objects\
            .filter(paid_for__month=today.month, paid_for__year=today.year)



