# Generated by Django 4.1.5 on 2023-09-29 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_alter_prescription_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='country',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='currency',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='department',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctorname',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.pharmcompany'),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.currency'),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='final_register',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.finalregister'),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.paymentmethod'),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.store'),
        ),
        migrations.AlterField(
            model_name='entrance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entrancethrough',
            name='entrance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.entrance'),
        ),
        migrations.AlterField(
            model_name='entrancethrough',
            name='medician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.medician'),
        ),
        migrations.AlterField(
            model_name='entrancethrough',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='finalregister',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='kind',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='market',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medician',
            name='big_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.bigcompany'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.country'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='medicines', to='core.department'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='kind',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.kind'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='pharm_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.pharmgroup'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.unit'),
        ),
        migrations.AlterField(
            model_name='medician',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicinewith',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.medician'),
        ),
        migrations.AlterField(
            model_name='patientname',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pharmcompany',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.city'),
        ),
        migrations.AlterField(
            model_name='pharmcompany',
            name='market',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.market'),
        ),
        migrations.AlterField(
            model_name='pharmcompany',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pharmgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prescriptionthrough',
            name='medician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.medician'),
        ),
        migrations.AlterField(
            model_name='prescriptionthrough',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='revenuetrough',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.prescription'),
        ),
        migrations.AlterField(
            model_name='revenuetrough',
            name='revenue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.revenue'),
        ),
        migrations.AlterField(
            model_name='revenuetrough',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PurchaseListManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('arrival', models.FloatField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('shortaged', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.medician')),
            ],
        ),
    ]