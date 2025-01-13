# Generated by Django 5.1.4 on 2025-01-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_cartbill_adults_cartbill_children_cartbill_infants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartbill',
            name='offer_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cartbill',
            name='offer_amount',
            field=models.FloatField(default=0.0),
        ),
    ]