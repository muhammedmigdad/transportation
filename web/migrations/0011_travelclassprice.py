# Generated by Django 5.1.4 on 2025-01-02 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_bus_date_flight_date_train_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelClassPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_class', models.CharField(choices=[('economy', 'Economy'), ('premium-economy', 'Premium Economy'), ('business', 'Business'), ('first-class', 'First Class')], max_length=20, unique=True, verbose_name='Travel Class')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
            ],
        ),
    ]
