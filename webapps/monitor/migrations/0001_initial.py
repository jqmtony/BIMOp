# Generated by Django 2.0 on 2018-01-05 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BIMComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, null=True)),
                ('content', models.CharField(max_length=200, null=True)),
                ('connectedFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.BIMComponent')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorType', models.CharField(max_length=200, null=True)),
                ('unit', models.CharField(max_length=200, null=True)),
                ('isDataFromBAS', models.BooleanField()),
                ('basAddress', models.CharField(max_length=200, null=True)),
                ('derivedSensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Sensor')),
                ('measuredTarget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.BIMComponent')),
            ],
        ),
        migrations.CreateModel(
            name='SensorDataHist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recordedTime', models.DateTimeField()),
                ('value', models.CharField(max_length=200, null=True)),
                ('isGood', models.BooleanField()),
                ('isBadNotes', models.CharField(max_length=200, null=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Sensor')),
            ],
        ),
    ]
