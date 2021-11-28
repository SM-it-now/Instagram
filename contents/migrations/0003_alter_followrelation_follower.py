# Generated by Django 3.2.9 on 2021-11-28 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0002_auto_20211129_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrelation',
            name='follower',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
