from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from .models import Note
from .serializers import NoteSerializer
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return Note.objects.all()
    #     raise PermissionDenied()
    #
    # # Set user as owner of a Notes object.
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

