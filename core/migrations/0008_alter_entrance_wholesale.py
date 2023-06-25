# Generated by Django 4.1.5 on 2023-06-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_entrance_wholesale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrance',
            name='wholesale',
            field=models.CharField(choices=[('WHOLESALE', 'WHOLESALE'), ('SINGULAR', 'SINGULAR')], default=1, max_length=100),
        ),
    ]
