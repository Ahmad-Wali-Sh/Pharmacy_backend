# Generated by Django 4.1.4 on 2023-01-16 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medician', '0002_unit_medician_image_medician_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namee', models.CharField(max_length=80)),
                ('code', models.IntegerField()),
                ('prescription_number', models.CharField(max_length=60)),
                ('medician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medician.medician')),
            ],
        ),
    ]