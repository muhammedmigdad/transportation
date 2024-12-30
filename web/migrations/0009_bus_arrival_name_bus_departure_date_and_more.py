# Generated by Django 5.1.4 on 2024-12-30 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_bus_total_seat_busseatstatus_delete_busseat'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='arrival_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='departure_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='arrival_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='train',
            name='arrival_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='train',
            name='departure_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='busseatstatus',
            name='buses',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='web.bus'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='arrival_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_code',
            field=models.CharField(max_length=100),
        ),
    ]
