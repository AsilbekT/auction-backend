# Generated by Django 5.1.3 on 2024-11-30 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Reference to the owner of the property being auctioned', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.owner'),
        ),
    ]
