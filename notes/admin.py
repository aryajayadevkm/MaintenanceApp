from django.contrib import admin

# Register your models here.
from .models import Note, Profile

admin.site.register(Note)
admin.site.register(Profile)