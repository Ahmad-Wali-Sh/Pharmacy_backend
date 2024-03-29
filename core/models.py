from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from image_optimizer.fields import OptimizedImageField
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
import random
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models import F
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.db.models import Q
import datetime
from jdatetime import datetime as jdatetime
from django.contrib.auth.models import Group
from core.utils import calculate_rounded_value
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.db.models.signals import m2m_changed, pre_delete, pre_save
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import json
from django.core.serializers.json import DjangoJSONEncoder
from barcode import Code39, Code128, EAN13, UPCA
import qrcode
from django.core.files.base import ContentFile

Group.add_to_class(
    "description", models.CharField(max_length=180, null=True, blank=True)
)


class AdditionalPermission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class GlobalSettings(models.Model):
    BARCODE_TYPES = (
        ('code39', 'Code39'),
        ('code128', 'Code128'),
        ('ean13', 'EAN13'),
        ('upca', 'UPCA'),
        ('qrcode', 'QR Code'),
    )

    barcode_type = models.CharField(max_length=10, choices=BARCODE_TYPES, default='code128')

    @classmethod
    def get_settings(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.create_default_settings()

    @classmethod
    def create_default_settings(cls):
        settings = cls.objects.create(barcode_type='code128')
        return settings


class User(AbstractUser):
    image = models.ImageField(
        null=True, blank=True, default="", upload_to="frontend/public/dist/images/users"
    )
    additional_permissions = models.ManyToManyField(AdditionalPermission, blank=True)
    REQUIRED_FIELDS = ["image", "email", "first_name", "last_name"]

    def get_additional_permissions(self):
        return ", ".join(str(p) for p in self.additional_permissions.all())

    get_additional_permissions.short_description = "Additional permissions"
    
    def __str__ (self):
        if (self.first_name and self.last_name):
            return self.first_name + ' ' + self.last_name
        elif (self.first_name):
            return self.first_name
        else:
            return self.username 


class ISODateTimeField(forms.DateTimeField):

    widget = DateTimeInput
    default_error_messages = {
        "invalid": _("Enter a valid date/time."),
    }

    def to_python(self, value):
        value = value.strip()
        try:
            return self.strptime(value, format)
        except (ValueError, TypeError):
            raise forms.ValidationError(self.error_messages["invalid"], code="invalid")

    def strptime(self, value, format):
        """stackoverflow won't let me save just an indent!"""
        return parse_datetime(force_str(value))


class Kind(models.Model):
    name_english = models.CharField(max_length=60, null=True, blank=True, unique=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/kinds",
        optimized_image_output_size=(500, 500),
        optimized_image_resize_method="cover",
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    # def __str__(self):
    #     if (self.name_english):
    #         return self.name_english
    #     elif (self.name_persian):
    #         return self.name_persian
    #     else: ''


class PharmGroup(models.Model):
    name_english = models.CharField(max_length=60, null=True, blank=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/pharm_groub",
        optimized_image_output_size=(500, 500),
        optimized_image_resize_method="cover",
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name_english


class Country(models.Model):
    name = models.CharField(max_length=50)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/countries",
        optimized_image_output_size=(500, 500),
        optimized_image_resize_method="cover",
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=240)
    over_price_money = models.FloatField(default=0)
    over_price_percent = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    celling_start = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class BigCompany(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


UNIQUE_ARRAY_FIELDS = ("barcode",)


class MyManager(models.Manager):
    def prevent_duplicates_in_array_fields(self, model, array_field):
        def duplicate_check(_lookup_params):
            fields = self.model._meta.get_fields()
            for unique_field in UNIQUE_ARRAY_FIELDS:
                unique_field_index = [getattr(field, "name", "") for field in fields]
                try:
                    # if model doesn't have the unique field, then proceed to the next loop iteration
                    unique_field_index = unique_field_index.index(unique_field)
                except ValueError:
                    continue
            all_items_in_db = [
                item
                for sublist in self.values_list(
                    fields[unique_field_index].name
                ).exclude(**_lookup_params)
                for item in sublist
            ]
            all_items_in_db = [item for sublist in all_items_in_db for item in sublist]
            if not set(array_field).isdisjoint(all_items_in_db):
                raise ValidationError(
                    "{} contains items already in the database".format(array_field)
                )

        if model.id:
            lookup_params = {"id": model.id}
        else:
            lookup_params = {}
        duplicate_check(lookup_params)


class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = ArrayField(
        models.CharField(max_length=400, blank=True, null=True),
        null=True,
        blank=True,
        default=list,
    )
    # barcode = models.CharField(max_length=255, null=True, blank=True, unique=True)
    barcode = ArrayField(
        models.CharField(max_length=255, null=True, blank=True),
        default=list,
        blank=True,
        null=True,
    )
    no_pocket = models.FloatField(null=True, blank=True)
    no_box = models.FloatField(null=True, default=1)
    pharm_group = models.ForeignKey(
        PharmGroup, on_delete=models.RESTRICT, null=True, blank=True
    )
    kind = models.ForeignKey(Kind, on_delete=models.RESTRICT, null=True, blank=True)
    ml = models.CharField(max_length=50, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, null=True, blank=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.RESTRICT, null=True, blank=True
    )
    company = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    last_purchased = models.FloatField(default=0)
    existence = models.FloatField(default=0, null=True, blank=True)
    minmum_existence = models.FloatField(blank=True, null=True, default=0)
    maximum_existence = models.FloatField(blank=True, null=True, default=0)
    must_advised = models.BooleanField(default=False)
    dividing_rules = models.TextField(blank=True, null=True)
    cautions = models.TextField(blank=True, null=True)
    usages = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/medician",
        optimized_image_output_size=(500, 500),
        optimized_image_resize_method="cover",
    )
    patient_approved = models.BooleanField(default=False)
    doctor_approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    department = models.ManyToManyField(Department, blank=True)
    min_expire_date = models.IntegerField(default=6, blank=True)
    big_company = models.ForeignKey(
        BigCompany, on_delete=models.RESTRICT, blank=True, null=True
    )
    shorted = models.BooleanField(default=False)
    to_buy = models.BooleanField(default=False)
    unsubmited_existence = models.FloatField(default=0)
    # objects = MyManager()

    # def __str__(self):
    #     return str(self.brand_name)

    def save(self, *args, **kwargs):
        if self.existence is None:
            self.existence = 0
        super().save(*args, **kwargs)


class MedicineBarcode(models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, unique=True)


GENDER_CHOICES = (("Male", "Male"), ("Female", "Female"))


class PatientName(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=1)
    birth_date = models.DateField(null=True, blank=True)
    tazkira_number = models.IntegerField(null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    sickness = models.CharField(max_length=100, null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class DoctorName(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    expertise = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    workplace = models.CharField(max_length=100, null=True, blank=True)
    work_time = models.CharField(max_length=100, null=True, blank=True)
    home_address = models.CharField(max_length=100, null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Revenue(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    zakat = models.FloatField(default=0)
    khairat = models.FloatField(default=0)
    rounded = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    start_time = models.TimeField(auto_now=False, null=True, blank=True)
    start_end = models.TimeField(auto_now=False, null=True, blank=True)
    start_end_date = models.DateField(null=True, blank=True, auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    employee = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="employee"
    )

    def update_model(self, *args, **kwargs):
        checkifopen = (
            Revenue.objects.filter(employee=self.employee)
            .filter(active=True)
            .filter(~Q(id=self.id))
        )
        if checkifopen:
            raise Exception("There is Already an Open Revenue...")
            pass
        else:
            super(Revenue, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.active == True:
            self.start_time = timezone.now().strftime("%H:%M:%S")
            self.start_end_date = ""
        else:
            self.start_end = timezone.now().strftime("%H:%M:%S")
        self.update_model()
        
    def __str__ (self):
        return 'Revenue: ' + str(self.id)


class Prescription(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.RESTRICT
    )  # انتخاب بخش فروش
    prescription_number = models.CharField(
        max_length=60, unique=True, null=True, blank=True, editable=False
    )
    name = models.ForeignKey(
        PatientName, on_delete=models.RESTRICT, null=True, blank=True
    )
    doctor = models.ForeignKey(
        DoctorName, on_delete=models.RESTRICT, null=True, blank=True
    )
    history = AuditlogHistoryField()
    medician = models.ManyToManyField(Medician, through="PrescriptionThrough")
    grand_total = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    over_money = models.FloatField(default=0)
    over_percent = models.FloatField(default=0)
    zakat = models.FloatField(default=0)
    khairat = models.FloatField(default=0)
    created = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    rounded_number = models.FloatField(default=0)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/prescriptions",
    )
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    refund = models.FloatField(default=0)
    barcode = models.ImageField(
        upload_to="frontend/public/dist/images/prescriptions/barcodes",
        blank=True,
        editable=False,
    )
    barcode_str = models.CharField(max_length=255, blank=True, editable=False)
    purchase_payment_date = models.DateTimeField(null=True, blank=True)
    purchased_value = models.FloatField(default=0)
    revenue = models.ForeignKey(
        Revenue, on_delete=models.RESTRICT, null=True, blank=True
    )
    order_user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, related_name='order_user')


    def __str__(self):
        return self.prescription_number

    def save(self, *args, **kwargs):
        if self.prescription_number:
            prescription_through_total = list(
                PrescriptionThrough.objects.filter(prescription_id=self.id)
                .aggregate(Sum("total_price"))
                .values()
            )[0]
            discount_percent = float(self.discount_percent)
            over_percent = float(self.over_percent)
            discount_amount = 0
            if prescription_through_total:
                discount_amount = prescription_through_total * (discount_percent / 100)
                over_amount = prescription_through_total * (over_percent / 100)
                self.rounded_number = calculate_rounded_value(
                    int(float(prescription_through_total)),
                    self.department.celling_start,
                )
                grand_total = (
                    float(prescription_through_total)
                    - discount_amount
                    - float(self.zakat)
                    - float(self.khairat)
                    - float(self.discount_money)
                    + float(self.rounded_number)
                    + over_amount
                    + float(self.over_money)
                )
                self.grand_total = round(grand_total, 0)

        if (
            self.sold
            and self.purchased_value != 0
            and (self.purchased_value != self.grand_total)
        ):
            self.refund = self.purchased_value - self.grand_total

        if self.purchased_value == self.grand_total:
            self.refund = 0

        if self.sold and self.refund == 0:
            self.purchase_payment_date = timezone.now()
            self.purchased_value = self.grand_total
        if not self.sold:
            self.purchase_payment_date = None

        # Now, you can access grand_total and calculate the rounded number

        # Get the current Jalali date
        today_jalali = jdatetime.now()
        start_jalali_date = jdatetime(today_jalali.year, today_jalali.month, 1)
        
        start_gregorian_date = start_jalali_date.togregorian()
        end_gregorian_date = today_jalali.togregorian()

        j_year = today_jalali.year
        j_month = today_jalali.month

        objects_count = Prescription.objects.filter(
            created__range=(start_gregorian_date, end_gregorian_date)
        ).count()

        count_of_month = objects_count + 1 if objects_count > 0 else 1

        if not self.prescription_number:
            if count_of_month == 1:
                self.prescription_number = f"{j_year}-{j_month:02d}-{count_of_month}"
            else:
                self.prescription_number = f"{j_year}-{j_month:02d}-{count_of_month}"

        if self.barcode_str == "":
            settings = GlobalSettings.get_settings()
            number = random.randint(1000000000000, 9999999999999)
            buffer = BytesIO()

            if settings.barcode_type == 'code39':
                code39 = Code39(f"{number}", writer=ImageWriter())
                code39.write(buffer)
                self.barcode_str = code39.get_fullcode()
                
            elif settings.barcode_type == 'qrcode':
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(str(number))
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                self.barcode.save(f"{number}.png", ContentFile(buffer.getvalue()), save=False)


            elif settings.barcode_type == 'code128':
                code128 = Code128(f"{number}", writer=ImageWriter())
                code128.write(buffer)
                self.barcode_str = code128.get_fullcode()

            elif settings.barcode_type == 'ean13':
                ean13 = EAN13(f"{number}", writer=ImageWriter())
                ean13.write(buffer)
                self.barcode_str = ean13.get_fullcode()

            elif settings.barcode_type == 'upca':
                upca = UPCA(f"{number}", writer=ImageWriter())
                upca.write(buffer)
                self.barcode_str = upca.get_fullcode()

            self.barcode.save(f"{number}" + ".png", File(buffer), save=False)

        return super().save(*args, **kwargs)
    
auditlog.register(Prescription, include_fields=['name', 'doctor', 'purchased_value', 'order_user','revenue', 'zakat', 'sold','khairat', 'discount_money', 'discount_percent', 'over_percent', 'over_money'],)


class PrescriptionImage(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/prescriptions",
    )


class PrescriptionThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    each_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.prescription.prescription_number

    def save(self, *args, **kwargs):
        """Calculation of Total Price for total_price field"""
        if self.quantity:
            self.total_price = round(self.quantity * self.each_price, 0)
        else:
            self.quantity = 1
            self.total_price = round(1 * self.each_price, 0)

        super(PrescriptionThrough, self).save(*args, **kwargs)

        if (
            self.prescription.refund == 0
            and self.prescription.purchased_value == 0
            and self.prescription.sold == True
        ):
            self.prescription.sold = False

        self.prescription.save()


class City(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PharmCompany(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=50, null=True, blank=True)
    ceo_phone = models.IntegerField(null=True, blank=True)
    manager = models.CharField(max_length=50, null=True, blank=True)
    manager_phone = models.IntegerField(null=True, blank=True)
    visitor = models.CharField(max_length=50, null=True, blank=True)
    visitor_phone = models.IntegerField(null=True, blank=True)
    companies = ArrayField(
        models.CharField(max_length=30, null=True, blank=True), null=True, blank=True
    )
    company_phone_1 = models.IntegerField(null=True, blank=True)
    company_phone_2 = models.IntegerField(null=True, blank=True)
    company_online = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.RESTRICT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=20)
    rate = models.FloatField()
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    responsible = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/stores",
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class FinalRegister(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


WHOLESALE_CHOICE = (("WHOLESALE", "WHOLESALE"), ("SINGULAR", "SINGULAR"))


class Entrance(models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.RESTRICT)
    factor_number = models.IntegerField(null=True, blank=True)
    medicians = models.ManyToManyField(Medician, through="EntranceThrough")
    factor_date = models.DateTimeField(default=timezone.now)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    total_interest = models.IntegerField()
    final_register = models.ForeignKey(FinalRegister, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    deliver_by = models.CharField(max_length=100, null=True, blank=True)
    recived_by = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    without_discount = models.BooleanField(default=False)
    discount_percent = models.FloatField(default=0)
    wholesale = models.CharField(max_length=100, choices=WHOLESALE_CHOICE, default=1)
    currency_rate = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs):
        if self.currency_rate == None:
            self.currency_rate = self.currency.rate

        super(Entrance, self).save(*args, **kwargs)


class EntranceImage(models.Model):
    entrance = models.ForeignKey(Entrance, on_delete=models.CASCADE)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/entrances",
    )


class EntranceThrough(models.Model):
    entrance = models.ForeignKey(Entrance, on_delete=models.RESTRICT)
    medician = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    number_in_factor = models.FloatField()
    each_price_factor = models.FloatField()
    each_price = models.FloatField(default=1)
    discount_money = models.FloatField(default=0)
    no_box = models.FloatField(default=1)
    discount_percent = models.FloatField(default=0)
    total_purchaseـafghani = models.FloatField(default=1)
    total_purchaseـcurrency = models.FloatField(default=1)
    total_purchase_currency_before = models.FloatField(default=0)
    discount_value = models.FloatField(default=0)
    each_quantity = models.FloatField(default=1)
    quantity_bonus = models.FloatField(default=0)
    bonus_value = models.FloatField(default=0)
    shortage = models.FloatField(default=0)
    lease = models.BooleanField(default=False)
    each_purchase_price = models.FloatField(default=1)
    each_sell_price = models.FloatField(default=0)
    each_sell_price_afg = models.FloatField(default=0)
    total_sell = models.FloatField(default=0)
    interest_percent = models.FloatField(default=20)
    register_quantity = models.IntegerField(default=0)
    total_interest = models.FloatField(default=0)
    expire_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    interest_money = models.FloatField(default=0)
    bonus_interest = models.FloatField(default=0)
    rate = models.FloatField(default=1)
    rate_name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.medician.brand_name + " - " + self.entrance.company.name + ".co"

    def save(self, *args, **kwargs):

        round_digit = 2

        self.total_purchase_currency_before = round(
            self.number_in_factor * self.each_price_factor, round_digit
        )
        self.total_purchaseـcurrency = round(
            self.total_purchase_currency_before * (1 - self.discount_percent / 100)
            - self.discount_money,
            round_digit,
        )
        self.discount_value = round(
            self.total_purchase_currency_before - self.total_purchaseـcurrency,
            round_digit,
        )
        # if (self.quantity_bonus > 0):
        #     self.bonus_value = round((self.total_purchase_currency_before / (
        #         self.number_in_factor + self.quantity_bonus)) * self.quantity_bonus, round_digit)
        # else:
        #     self.bonus_value = 0
        self.each_purchase_price = round(
            (self.each_price_factor / self.no_box), round_digit
        )
        self.each_price = round(
            self.each_purchase_price * (1 + self.interest_percent / 100), round_digit
        )
        self.register_quantity = (
            (self.number_in_factor * self.no_box) - (self.shortage * self.no_box)
        ) + self.quantity_bonus
        self.each_sell_price = round(
            self.each_sell_price_afg / self.entrance.currency_rate, round_digit
        )
        self.bonus_value = self.each_sell_price * self.quantity_bonus
        self.total_sell = round(
            self.each_price * self.no_box * self.number_in_factor + self.bonus_value,
            round_digit,
        )
        self.rate = self.entrance.currency_rate
        self.rate_name = self.entrance.currency.name

        self.medician.last_purchased = self.each_purchase_price
        self.medician.save()

        super(EntranceThrough, self).save(*args, **kwargs)


class Outrance(models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.CASCADE)
    factor_number = models.IntegerField()
    medicians = models.ManyToManyField(Medician, through="OutranceThrough")
    factor_date = models.DateField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    total_interest = models.IntegerField()
    final_register = models.ForeignKey(FinalRegister, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    deliver_by = models.CharField(max_length=100)
    recived_by = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    without_discount = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name


class OutranceThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    outrance = models.ForeignKey(Outrance, on_delete=models.CASCADE)
    number_in_factor = models.IntegerField()  # G4 تعداد در فاکتور
    each_price_factor = models.FloatField()  # G8 قیمت فی خرید توسط کاربر
    each_price = models.FloatField(default=1)  # G5 قیمت فی خرید فاکتور
    discount_money = models.FloatField(default=0)  # G6 تخفیف خرید پولی
    discount_percent = models.FloatField(default=0)  # G7 تخفیف خرید فیصدی
    total_purchaseـafghani = models.FloatField(default=1)  # G9 مجموع خرید افغانی
    total_purchaseـcurrency = models.FloatField(default=1)  # G10 مجموع خرید اسعاری
    each_quantity = models.IntegerField(default=1)  # G11  تعداد در فی فروش
    bonus = models.IntegerField(default=0)  # G12 بونوس
    quantity_bonus = models.IntegerField(default=0)  # G13 تعداد بیشتر از خرید
    register_quantity = models.IntegerField(
        default=0
    )  # G14 تعداد ثبت به سیستم جهت موجودی
    each_purchase_price = models.FloatField(
        default=1
    )  # G18 قیمت فی خرید جهت ثبت به سیستم
    interest_money = models.FloatField(default=0)  # G19 فایده پولی
    interest_percent = models.FloatField(default=20)  # G20 فایده فیصدی
    each_sell_price = models.FloatField(default=0)  # G21 قیمت فی فروش جهت ثبت به سیستم
    total_sell = models.FloatField(default=0)  # G25 مجموع فروش
    bonus_interest = models.FloatField(default=0)  # G27 مجموع فروش بونوس دار
    total_interest = models.FloatField(default=0)  # G30 مجموع فایده
    expire_date = models.DateField()  # G31 تاریخ انقضا
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.medician.brand_name + " - " + self.outrance.company.name + ".co"


class RevenueTrough(models.Model):
    revenue = models.ForeignKey(Revenue, on_delete=models.DO_NOTHING)
    prescription = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.FloatField(default=0)
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if self.prescription.refund == 0:
            self.purchased = self.prescription.grand_total
        if self.prescription.refund != 0:
            self.purchased = self.prescription.refund
            self.prescription.sold = True
            self.prescription.refund = 0

        if self.sold == True:
            self.prescription.sold = True
            self.prescription.save()

        super(RevenueTrough, self).save()

    # class Meta:
    #     unique_together = ('revenue', 'prescription',)


class PurchaseList(models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.DO_NOTHING)
    need_quautity = models.FloatField(default=0)
    company_1 = models.ForeignKey(PharmCompany, on_delete=models.DO_NOTHING)
    price_1 = models.FloatField(default=0)
    bonus_1 = models.FloatField(default=0)
    date_1 = models.DateField()
    company_2 = models.ForeignKey(
        PharmCompany, on_delete=models.DO_NOTHING, related_name="company_2"
    )
    price_2 = models.FloatField(default=0)
    bonus_2 = models.FloatField(default=0)
    date_2 = models.DateField()
    company_3 = models.ForeignKey(
        PharmCompany, on_delete=models.DO_NOTHING, related_name="company_3"
    )
    price_3 = models.FloatField(default=0)
    bonus_3 = models.FloatField(default=0)
    date_3 = models.DateField()
    arrival_quantity = models.FloatField(default=0)
    shortaged = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine.brand_name


class MedicineWith(models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    includes = models.ManyToManyField(Medician, related_name="medicines")

    def __str__(self):
        return self.medicine.brand_name


class MedicineConflict(models.Model):
    medicine_1 = models.ForeignKey(
        Medician, on_delete=models.DO_NOTHING, related_name="medicine_1"
    )
    medicine_2 = models.ForeignKey(Medician, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.medicine_1.brand_name + " vs " + self.medicine_2.brand_name


class PurchaseListManual(models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.CASCADE)
    quantity = models.FloatField()
    arrival = models.FloatField(default=0)
    approved = models.BooleanField(default=False)
    shortaged = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.medicine.brand_name

    def save(self, *args, **kwargs):
        if self.arrival > 0:
            self.approved = True
            self.medicine.unsubmited_existence = self.arrival
            self.medicine.save()
        if self.arrival == 0:
            self.approved = False
            self.medicine.unsubmited_existence = self.arrival
            self.medicine.save()
        super(PurchaseListManual, self).save(*args, **kwargs)

@receiver(post_delete, sender=PrescriptionThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):

    prescription_through_total = list(
        PrescriptionThrough.objects.filter(prescription_id=instance.prescription.id)
        .aggregate(Sum("total_price"))
        .values()
    )[0]
    discount_percent = float(instance.prescription.discount_percent)
    over_percent = float(instance.prescription.over_percent)
    if prescription_through_total:
        discount_amount = prescription_through_total * (discount_percent / 100)
        over_amount = prescription_through_total * (over_percent / 100)
        grand_total = (
            float(prescription_through_total)
            - discount_amount
            - float(instance.prescription.zakat)
            - float(instance.prescription.khairat)
            - float(instance.prescription.discount_money)
            + float(instance.prescription.rounded_number)
            + over_amount
            + float(instance.prescription.over_money)
        )
    else:
        grand_total = 0

    if prescription_through_total and grand_total:
        instance.prescription.grand_total = round(grand_total, 0)

    instance.prescription.save()


@receiver(post_delete, sender=PrescriptionThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):
    prescription_through_total = list(
        PrescriptionThrough.objects.filter(prescription_id=instance.prescription.id)
        .aggregate(Sum("total_price"))
        .values()
    )[0]

    if prescription_through_total:
        instance.prescription.grand_total = prescription_through_total
        instance.prescription.save()
    else:
        instance.prescription.grand_total = 0
        instance.prescription.save()

    instance.medician.save()


# def get_medicine_full(res):
#     obj = res
#     kind_name = obj.kind.name_english if obj and obj.kind and obj.kind.name_english else ""
#     country_name = obj.country.name if obj and obj.country else ""
#     big_company_name = obj.big_company.name if obj and obj.big_company else ""
#     generics = "{" + ",".join(map(str, obj.generic_name)) + "}" if obj and obj.generic_name else ""
#     ml = str(obj.ml) if obj and obj.ml else ""
#     weight = str(obj.weight) if obj and obj.weight else ""
    
    
#     result = ".".join(filter(None, [kind_name, obj.brand_name.strip(), ml, big_company_name, country_name, weight]))
#     print(result)
#     return result.strip()

def get_medicine_full(res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country and obj.country.name:
            country_name = obj.country.name
        if obj.big_company and obj.big_company.name:
            big_company_name = obj.big_company.name + " "
        if obj.generic_name:
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if obj.ml:
            ml = obj.ml
        if obj.weight:
            weight = obj.weight

        return (
            kind_name
            + obj.brand_name
            + " "
            + ml
            + " "
            + big_company_name
            + country_name
            + " "
            + weight
        ).strip()


def get_prescription_through_data(prescription_through):
    return {
        'medician_id': prescription_through.medician_id,
        'quantity': prescription_through.quantity,
        'medician_name': get_medicine_full(prescription_through.medician),
        'each_price': prescription_through.each_price,
        'total_price': prescription_through.total_price,
    }
        
@receiver(pre_save, sender=PrescriptionThrough)
@receiver(pre_delete, sender=PrescriptionThrough)
def prescription_through_changed(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return

    changes = {}

    if instance.pk:
        try:
            previous_instance = PrescriptionThrough.objects.get(pk=instance.pk)
        except PrescriptionThrough.DoesNotExist:
            # This is a new instance, so we don't have previous data
            changes = dict(
                prescription_through=dict(new=get_prescription_through_data(instance)),
            )
        else:
            current_data = get_prescription_through_data(instance)
            previous_data = get_prescription_through_data(previous_instance)

            if (
                previous_data['medician_id'] != current_data['medician_id']
                or previous_data['quantity'] != current_data['quantity']
                or previous_data['each_price'] != current_data['each_price']
                or previous_data['total_price'] != current_data['total_price']
            ):
                changes = dict(
                    prescription_through=dict(old=previous_data, new=current_data),
                )

        if changes:
            LogEntry.objects.create(
                object_id=instance.prescription_id,
                content_type=ContentType.objects.get_for_model(instance.prescription),
                actor_id=instance.prescription.user_id,
                action=1 if previous_instance else 0,  # Action flag for update or creation
                changes=json.dumps(changes, cls=DjangoJSONEncoder),
            )

    elif kwargs.get('signal') == pre_delete:
        changes = dict(
            prescription_through=dict(old=get_prescription_through_data(instance)),
        )

        LogEntry.objects.create(
            object_id=instance.prescription_id,
            content_type=ContentType.objects.get_for_model(instance.prescription),
            actor_id=instance.prescription.user_id,
            action=2,  # Action flag for deletion
            changes=json.dumps(changes, cls=DjangoJSONEncoder),
        )
        
@receiver(post_save, sender=PrescriptionThrough)
def prescription_through_post_save(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return

    if created:
        changes = dict(
            prescription_through=dict(new=get_prescription_through_data(instance)),
        )

        LogEntry.objects.create(
            object_id=instance.prescription_id,
            content_type=ContentType.objects.get_for_model(instance.prescription),
            actor_id=instance.prescription.user_id,
            action=0,  # Action flag for creation
            changes=json.dumps(changes, cls=DjangoJSONEncoder),
        )
    else:
        try:
            previous_instance = PrescriptionThrough.objects.get(pk=instance.pk)
        except PrescriptionThrough.DoesNotExist:
            pass
        else:
            current_data = get_prescription_through_data(instance)
            previous_data = get_prescription_through_data(previous_instance)

            if (
                previous_data['medician_id'] != current_data['medician_id']
                or previous_data['quantity'] != current_data['quantity']
                or previous_data['each_price'] != current_data['each_price']
                or previous_data['total_price'] != current_data['total_price']
            ):
                changes = dict(
                    prescription_through=dict(old=previous_data, new=current_data),
                )

                LogEntry.objects.create(
                    object_id=instance.prescription_id,
                    content_type=ContentType.objects.get_for_model(instance.prescription),
                    actor_id=instance.prescription.user_id,
                    action=1,  # Action flag for update
                    changes=json.dumps(changes, cls=DjangoJSONEncoder),
                )

@receiver(post_delete, sender=PrescriptionThrough)
def prescription_through_post_delete(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return

    changes = dict(
        prescription_through=dict(old=get_prescription_through_data(instance)),
    )

    LogEntry.objects.create(
        object_id=instance.prescription_id,
        content_type=ContentType.objects.get_for_model(instance.prescription),
        actor_id=instance.prescription.user_id,
        action=2,  # Action flag for deletion
        changes=json.dumps(changes, cls=DjangoJSONEncoder),
    )
    
@receiver([post_save, post_delete], sender=EntranceThrough)
@receiver([post_save, post_delete], sender=PrescriptionThrough)
def update_medician_existence(sender, instance, **kwargs):
    medician = instance.medician
    entrance_sum_query = (
        EntranceThrough.objects.filter(medician_id=medician.id)
        .aggregate(Sum("register_quantity"))
        .get("register_quantity__sum", 0)
    )
    prescription_sum_query = (
        PrescriptionThrough.objects.filter(medician_id=medician.id)
        .aggregate(Sum("quantity"))
        .get("quantity__sum", 0)
    )

    entrance_sum = entrance_sum_query if entrance_sum_query is not None else 0
    prescription_sum = (
        prescription_sum_query if prescription_sum_query is not None else 0
    )

    existence = entrance_sum - prescription_sum
    if existence is None:
        existence = 0
    medician.existence = round(existence, 1)

    # Update unsubmited_existence based on comparison with entrance quantity
    if existence >= medician.unsubmited_existence:
        medician.unsubmited_existence = 0

    medician.save()