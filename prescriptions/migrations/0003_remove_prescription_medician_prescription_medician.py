# Generated by Django 4.1.4 on 2023-01-16 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medician', '0002_unit_medician_image_medician_unit'),
        ('prescriptions', '0002_rename_namee_prescription_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medician',
        ),
        migrations.AddField(
            model_name='prescription',
            name='medician',
            field=models.ManyToManyField(to='medician.medician'),
        ),
    ]
