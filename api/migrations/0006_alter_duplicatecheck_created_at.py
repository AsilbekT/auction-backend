# Generated by Django 5.1.3 on 2024-12-04 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_reformated_address_duplicatecheck_reformatted_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicatecheck',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
