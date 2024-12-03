# Generated by Django 5.1.3 on 2024-11-30 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_salesinformation_property_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='property',
            field=models.ForeignKey(help_text='Reference to the property being auctioned', on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='api.property'),
        ),
    ]