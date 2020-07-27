from django.contrib import admin

# Register your models here.
from .models import Flat, Resident

admin.site.register(Flat)
admin.site.register(Resident)