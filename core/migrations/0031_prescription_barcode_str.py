# Generated by Django 4.1.5 on 2023-09-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_prescription_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='barcode_str',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
