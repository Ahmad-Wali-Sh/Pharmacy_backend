# Generated by Django 4.1.4 on 2023-01-14 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Pharm_Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Medician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('generic_name', models.CharField(blank=True, max_length=100, null=True)),
                ('no_pocket', models.IntegerField()),
                ('ml', models.FloatField()),
                ('weight', models.FloatField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.FloatField()),
                ('minmum_existence', models.FloatField()),
                ('maximum_existence', models.FloatField()),
                ('dividing_rules', models.TextField(blank=True, null=True)),
                ('cautions', models.TextField(blank=True, null=True)),
                ('usages', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medician.country')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medician.kind')),
                ('pharm_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medician.pharm_group')),
            ],
        ),
    ]