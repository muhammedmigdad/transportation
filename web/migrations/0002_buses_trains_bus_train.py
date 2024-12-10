# Generated by Django 5.1.4 on 2024-12-10 10:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Trains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='bus_images/')),
                ('bus_numbers', models.CharField(max_length=100)),
                ('departure_time', models.TimeField()),
                ('departure_code', models.CharField(max_length=10)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=7200))),
                ('stops', models.CharField(max_length=50)),
                ('arrival_time', models.TimeField()),
                ('arrival_code', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.airlines')),
            ],
            options={
                'verbose_name': 'bus',
                'verbose_name_plural': 'buses',
                'db_table': 'bus',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='train_images/')),
                ('train_numbers', models.CharField(max_length=100)),
                ('departure_time', models.TimeField()),
                ('departure_code', models.CharField(max_length=10)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=7200))),
                ('stops', models.CharField(max_length=50)),
                ('arrival_time', models.TimeField()),
                ('arrival_code', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.airlines')),
            ],
            options={
                'verbose_name': 'train',
                'verbose_name_plural': 'trains',
                'db_table': 'train',
                'ordering': ['-id'],
            },
        ),
    ]
