from rest_framework import serializers
from .models import Note, Profile


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "flat_no","owner")
        model = Note


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    flats = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = ('username', 'mobile_no', 'flats')
        read_only_fields = ('username',)

