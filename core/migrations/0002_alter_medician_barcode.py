# Generated by Django 4.1.5 on 2023-06-20 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medician',
            name='barcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
