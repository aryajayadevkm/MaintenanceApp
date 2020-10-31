from django.contrib import admin

# Register your models here.
from .models import User, Building


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'no_of_flats')


admin.site.register(User, UserAdmin)
admin.site.register(Building, BuildingAdmin)
