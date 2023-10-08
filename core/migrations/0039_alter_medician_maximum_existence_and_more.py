# Generated by Django 4.2.5 on 2023-10-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_medician_maximum_existence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medician',
            name='maximum_existence',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medician',
            name='minmum_existence',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]