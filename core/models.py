from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from image_optimizer.fields import OptimizedImageField
from django.contrib.auth.models import User
from django.utils import timezone
import random
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.db.models import Q
from jdatetime import datetime as jdatetime
from django.contrib.auth.models import Group
from core.utils import calculate_rounded_value
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
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
        ("code39", "Code39"),
        ("code128", "Code128"),
        ("ean13", "EAN13"),
        ("upca", "UPCA"),
        ("qrcode", "QR Code"),
    )

    barcode_type = models.CharField(
        max_length=10, choices=BARCODE_TYPES, default="code128"
    )

    @classmethod
    def get_settings(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.create_default_settings()

    @classmethod
    def create_default_settings(cls):
        settings = cls.objects.create(barcode_type="code128")
        return settings


class User(AbstractUser):
    image = models.ImageField(
        null=True, blank=True, default="", upload_to="frontend/public/dist/images/users"
    )
    additional_permissions = models.ManyToManyField(AdditionalPermission, blank=True)
    REQUIRED_FIELDS = ["image", "email", "first_name", "last_name", 'hourly_rate']
    hourly_rate = models.FloatField(null=True, blank=True)

    def get_additional_permissions(self):
        return ", ".join(str(p) for p in self.additional_permissions.all())

    get_additional_permissions.short_description = "Additional permissions"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name:
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

    def __str__(self):
        if self.name_english:
            return self.name_english
        elif self.name_persian:
            return self.name_persian
        else:
            return ""


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


class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = ArrayField(
        models.CharField(max_length=400, blank=True, null=True),
        null=True,
        blank=True,
        default=list,
    )
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

    def save(self, *args, **kwargs):
        if self.existence is None:
            self.existence = 0
        super().save(*args, **kwargs)

    def get_medicine_full(self, obj):
        kind_name = f"{obj.kind.name_english}." if obj.kind else ""
        country_name = f"{obj.country.name}" if obj.country else ""
        big_company_name = f"{obj.big_company.name} " if obj.big_company else ""
        generics = (
            f"{{{','.join(map(str, obj.generic_name))}}}" if obj.generic_name else ""
        )
        ml = f"{obj.ml}" if obj.ml else ""
        weight = f"{obj.weight}" if obj.weight else ""

        medicine_full = f"{kind_name}{obj.brand_name} {ml} {big_company_name} {country_name} {weight}"
        return medicine_full


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

    def __str__(self):
        return "Revenue: " + str(self.id)


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
    order_user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="order_user",
    )

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

        purchased_total = (
            RevenueRecord.objects.filter(prescription=self.id, prescription_return__isnull=True)
            .aggregate(total=Sum("amount"))
            .get("total") or 0
        )

        if purchased_total :
            self.purchased_value = purchased_total
            self.refund = self.grand_total - purchased_total
        else:
            self.purchased_value = 0
            self.refund = self.grand_total

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

            if settings.barcode_type == "code39":
                code39 = Code39(f"{number}", writer=ImageWriter())
                self.barcode_str = code39.get_fullcode()

            elif settings.barcode_type == "code128":
                code128 = Code128(f"{number}", writer=ImageWriter())
                self.barcode_str = code128.get_fullcode()

            elif settings.barcode_type == "ean13":
                ean13 = EAN13(f"{number}", writer=ImageWriter())
                self.barcode_str = ean13.get_fullcode()

            elif settings.barcode_type == "upca":
                upca = UPCA(f"{number}", writer=ImageWriter())
                self.barcode_str = upca.get_fullcode()

        return super().save(*args, **kwargs)


# Prescriptio Returns Models...


class DepartmentReturn(models.Model):
    name = models.CharField(max_length=240)
    over_price_money = models.FloatField(default=0)
    over_price_percent = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    celling_start = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PrescriptionReturn(models.Model):
    department = models.ForeignKey(DepartmentReturn, on_delete=models.RESTRICT)
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
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    refund = models.FloatField(default=0)
    barcode_str = models.CharField(max_length=255, blank=True, editable=False)
    purchase_payment_date = models.DateTimeField(null=True, blank=True)
    purchased_value = models.FloatField(default=0)
    revenue = models.ForeignKey(
        Revenue, on_delete=models.RESTRICT, null=True, blank=True
    )
    order_user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="prescription_order_user",
    )

    def __str__(self):
        return self.prescription_number

    def save(self, *args, **kwargs):
        if self.prescription_number:
            prescription_through_total = list(
                PrescriptionReturnThrough.objects.filter(prescription_id=self.id)
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
                grand_total = -(
                    float(prescription_through_total)
                    - discount_amount
                    - float(self.zakat)
                    - float(self.khairat)
                    - float(self.discount_money)
                    + float(self.rounded_number)
                    + over_amount
                    + float(self.over_money)
                )
                self.grand_total = round(grand_total, 1)
                
        purchased_total = (
            RevenueRecord.objects.filter(prescription_return=self.id, prescription__isnull=True)
            .aggregate(total=Sum("amount"))
            .get("total") or 0
        )

        if purchased_total :
            self.purchased_value = purchased_total
            self.refund = self.grand_total - purchased_total
        else:
            self.purchased_value = 0
            self.refund = self.grand_total

        today_jalali = jdatetime.now()
        start_jalali_date = jdatetime(today_jalali.year, today_jalali.month, 1)

        start_gregorian_date = start_jalali_date.togregorian()
        end_gregorian_date = today_jalali.togregorian()

        j_year = today_jalali.year
        j_month = today_jalali.month

        objects_count = PrescriptionReturn.objects.filter(
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

            if settings.barcode_type == "code39":
                code39 = Code39(f"{number}", writer=ImageWriter())
                self.barcode_str = code39.get_fullcode()

            elif settings.barcode_type == "code128":
                code128 = Code128(f"{number}", writer=ImageWriter())
                self.barcode_str = code128.get_fullcode()

            elif settings.barcode_type == "ean13":
                ean13 = EAN13(f"{number}", writer=ImageWriter())
                self.barcode_str = ean13.get_fullcode()

            elif settings.barcode_type == "upca":
                upca = UPCA(f"{number}", writer=ImageWriter())
                self.barcode_str = upca.get_fullcode()

        return super().save(*args, **kwargs)


auditlog.register(
    PrescriptionReturn,
    include_fields=[
        "name",
        "doctor",
        "purchased_value",
        "order_user",
        "revenue",
        "zakat",
        "sold",
        "khairat",
        "discount_money",
        "discount_percent",
        "over_percent",
        "over_money",
    ],
)


class PrescriptionReturnImage(models.Model):
    prescription = models.ForeignKey(PrescriptionReturn, on_delete=models.CASCADE)
    image = OptimizedImageField(
        null=True,
        blank=True,
        default="",
        upload_to="frontend/public/dist/images/prescription_returns",
    )


class PrescriptionReturnThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    prescription = models.ForeignKey(PrescriptionReturn, on_delete=models.CASCADE)
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

        super(PrescriptionReturnThrough, self).save(*args, **kwargs)

        self.prescription.save()


# Prescription Return End


class RevenueRecord(models.Model):
    revenue = models.ForeignKey(Revenue, on_delete=models.RESTRICT)
    prescription = models.ForeignKey(
        Prescription, null=True, blank=True, on_delete=models.RESTRICT
    )
    prescription_return = models.ForeignKey(
        PrescriptionReturn, null=True, blank=True, on_delete=models.RESTRICT
    )
    record_type = models.CharField(max_length=30)
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        if (self.prescription):            
            return str(self.revenue.id) + " | " + str(self.prescription.prescription_number)
        if (self.prescription_return):
            return str(self.revenue.id) + " | " + str(self.prescription_return.prescription_number)
        else: str(self.revenue.id)

auditlog.register(
    Prescription,
    include_fields=[
        "name",
        "doctor",
        "purchased_value",
        "order_user",
        "revenue",
        "zakat",
        "sold",
        "khairat",
        "discount_money",
        "discount_percent",
        "over_percent",
        "over_money",
    ],
)


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

        super(EntranceThrough, self).save(*args, **kwargs)


class MedicineWith(models.Model):
    medician = models.ForeignKey(
        Medician, on_delete=models.RESTRICT, related_name="add_medicine"
    )
    additional = models.ManyToManyField(Medician, blank=True, null=True)

    def __str__(self):
        return self.medician.brand_name


class MedicineSaleDictionary(models.Model):
    medician = models.ForeignKey(
        Medician, on_delete=models.RESTRICT, related_name="list_medicine"
    )
    sale = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.medician.brand_name


class MedicineConflict(models.Model):
    medicine_1 = models.ForeignKey(
        Medician, on_delete=models.DO_NOTHING, related_name="medicine_1"
    )
    medicine_2 = models.ForeignKey(Medician, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.medicine_1.brand_name + " vs " + self.medicine_2.brand_name


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
        
class JournalCategory(models.Model):
    name = models.CharField(max_length=150)
    info = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)   
    
    def __str__(self):
        return self.name  
         
class JournalEntry(models.Model):
    related_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='related_user')
    amount = models.FloatField(default=0)
    category = models.ForeignKey(JournalCategory, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    history = AuditlogHistoryField()
    
    def __str__(self):
        return f'{self.related_user}: {self.amount}, {self.category.name}'
    
auditlog.register(
    JournalEntry,
    include_fields=[
        "related_user",
        "amount",
        "category",
        "description",
        'user'
    ]
)

class SalaryEntry(models.Model):
    employee = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='salary_employee')
    payment_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    hourly_rate = models.FloatField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    penalty = models.FloatField(null=True, blank=True)
    bonus = models.FloatField(null=True, blank=True)
    checked = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='user')
    
    def __str__(self):
        return f"Salary for {self.employee.first_name} on {self.payment_date} - {self.amount}"
    

from . import signals
