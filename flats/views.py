import jwt
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import Flat, Resident, PaymentHistory
from .serializers import FlatSerializer, ResidentSerializer, DisplayCollectionSerializer, \
    MakePaymentSerializer, CreateFlatSerializer


# class IsSuperUser(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user and request.user.is_superuser
#
#
# class IsOwner(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user

class IsAuthorised(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        payload = jwt.decode(request.token, settings.SECRET_KEY)
        print(obj.building)
        print(payload)
        return obj.building == payload['building'], payload


class FlatViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def retrieve(self, request, pk):
        instance = Flat.objects.get(pk=pk)
        serializer = FlatSerializer(instance)
        return Response(serializer.data)

    def list(self, request):
        queryset = Flat.objects.all()
        serializer = FlatSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = CreateFlatSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        data = request.data
        instance = Flat.objects.get(pk=pk)
        serializer = CreateFlatSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResidentListViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ResidentSerializer
    queryset = Resident.objects.all()



class MonthlyCollectionListCreateView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk):
        instance = Flat.objects.get(pk=pk)
        serializer = DisplayCollectionSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Flat.objects.all()
        serializer = DisplayCollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk):
        instance = Flat.objects.get(pk=pk)
        serializer = MakePaymentSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
