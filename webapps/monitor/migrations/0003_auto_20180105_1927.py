# Generated by Django 2.0 on 2018-01-05 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20180105_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bimcomponent',
            name='connectedFrom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.BIMComponent'),
        ),
    ]