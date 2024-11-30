# Generated by Django 5.1.3 on 2024-11-30 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_legalproceeding_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownership',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='api.owner'),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='api.property'),
        ),
    ]
