# Generated by Django 4.1.4 on 2023-01-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medician', '0003_alter_medician_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medician',
            name='ml',
            field=models.CharField(max_length=50),
        ),
    ]