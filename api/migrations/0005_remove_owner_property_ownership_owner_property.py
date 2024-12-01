# Generated by Django 5.1.3 on 2024-11-30 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_auction_legal_remove_auction_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='property',
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage_owned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('date_acquired', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.owner')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.property')),
            ],
        ),
        migrations.AddField(
            model_name='owner',
            name='property',
            field=models.ManyToManyField(through='api.Ownership', to='api.property'),
        ),
    ]
