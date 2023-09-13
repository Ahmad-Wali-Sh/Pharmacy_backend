# Generated by Django 4.1.5 on 2023-09-13 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_prescription_barcode_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.department'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.doctorname'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.patientname'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
