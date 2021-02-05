# Generated by Django 3.1.6 on 2021-02-05 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_hike_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hike',
            name='likes',
            field=models.ManyToManyField(related_name='user_hike', to=settings.AUTH_USER_MODEL),
        ),
    ]