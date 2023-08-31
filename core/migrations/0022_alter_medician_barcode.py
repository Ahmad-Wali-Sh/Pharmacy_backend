# Generated by Django 4.1.5 on 2023-08-31 11:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_medician_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medician',
            name='barcode',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, default='', null=True, size=None),
        ),
    ]
