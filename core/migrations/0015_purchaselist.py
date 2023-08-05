# Generated by Django 4.1.5 on 2023-08-05 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_medicineconflict'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_quautity', models.FloatField(default=0)),
                ('price_1', models.FloatField(default=0)),
                ('bonus_1', models.FloatField(default=0)),
                ('date_1', models.DateField()),
                ('price_2', models.FloatField(default=0)),
                ('bonus_2', models.FloatField(default=0)),
                ('date_2', models.DateField()),
                ('price_3', models.FloatField(default=0)),
                ('bonus_3', models.FloatField(default=0)),
                ('date_3', models.DateField()),
                ('arrival_quantity', models.FloatField(default=0)),
                ('shortaged', models.BooleanField(default=False)),
                ('company_1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.pharmcompany')),
                ('company_2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='company_2', to='core.pharmcompany')),
                ('company_3', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='company_3', to='core.pharmcompany')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.medician')),
            ],
        ),
    ]
