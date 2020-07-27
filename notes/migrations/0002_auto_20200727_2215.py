# Generated by Django 3.0.8 on 2020-07-27 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='flat',
        ),
        migrations.AlterField(
            model_name='note',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flats', to=settings.AUTH_USER_MODEL),
        ),
    ]
