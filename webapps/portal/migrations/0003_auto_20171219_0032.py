# Generated by Django 2.0 on 2017-12-19 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20171218_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwrapper',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
