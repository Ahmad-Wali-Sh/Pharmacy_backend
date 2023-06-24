# Generated by Django 4.1.5 on 2023-06-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_entrance_wholesale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrance',
            name='wholesale',
            field=models.CharField(choices=[('WHOLESALE', 1), ('SINGULAR', 2)], default=1, max_length=100),
        ),
    ]
