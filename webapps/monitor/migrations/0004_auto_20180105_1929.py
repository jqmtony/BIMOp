# Generated by Django 2.0 on 2018-01-05 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20180105_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='basAddress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='derivedSensor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Sensor'),
        ),
    ]
