# Generated by Django 4.1.5 on 2023-05-25 13:58

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_doctorname_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrance',
            name='factor_date',
            field=django_jalali.db.models.jDateField(),
        ),
    ]
