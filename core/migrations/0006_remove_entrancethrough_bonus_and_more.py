# Generated by Django 4.1.5 on 2023-07-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_revenuetrough_unique_together_medicinewith'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrancethrough',
            name='bonus',
        ),
        migrations.AddField(
            model_name='entrancethrough',
            name='bonus_value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='entrancethrough',
            name='discount_value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='entrancethrough',
            name='shortage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='entrancethrough',
            name='total_purchase_currency_before',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='entrancethrough',
            name='quantity_bonus',
            field=models.FloatField(default=0),
        ),
    ]
