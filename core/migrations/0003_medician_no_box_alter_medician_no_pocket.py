# Generated by Django 4.1.5 on 2023-06-15 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_prescription_prescription_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='medician',
            name='no_box',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medician',
            name='no_pocket',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
