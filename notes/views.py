from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from .models import Flat
from .serializers import FlatSerializer
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return Note.objects.all()
    #     raise PermissionDenied()
    #
    # # Set user as owner of a Notes object.
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

