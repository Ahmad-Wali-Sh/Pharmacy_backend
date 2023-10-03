# Generated by Django 4.2.5 on 2023-10-03 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_revenue_start_end_date_alter_kind_name_english_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medician',
            name='maximum_existence',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='medician',
            name='minmum_existence',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
