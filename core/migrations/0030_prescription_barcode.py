# Generated by Django 4.1.5 on 2023-09-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_prescription_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='barcode',
            field=models.ImageField(blank=True, upload_to='frontend/public/dist/images/prescriptions/barcodes'),
        ),
    ]
