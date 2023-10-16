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
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.db.models import Q
import datetime


class User(AbstractUser):
    image = models.ImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/users')
    REQUIRED_FIELDS = ['image', 'email', 'first_name', 'last_name']


class ISODateTimeField(forms.DateTimeField):

    widget = DateTimeInput
    default_error_messages = {
        'invalid': _('Enter a valid date/time.'),
    }

    def to_python(self, value):
        value = value.strip()
        try:
            return self.strptime(value, format)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                self.error_messages['invalid'], code='invalid')

    def strptime(self, value, format):
        """ stackoverflow won't let me save just an indent! """
        return parse_datetime(force_str(value))


class Kind(models.Model):
    name_english = models.CharField(max_length=60, null=True, blank=True, unique=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/kinds', optimized_image_output_size=(500, 500),
        optimized_image_resize_method="cover")
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name_english


class PharmGroup(models.Model):
    name_english = models.CharField(max_length=60, null=True, blank=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/pharm_groub', optimized_image_output_size=(500, 500),
                                optimized_image_resize_method="cover")
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name_english


class Country(models.Model):
    name = models.CharField(max_length=50)
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/countries', optimized_image_output_size=(500, 500),
                                optimized_image_resize_method="cover")
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Department (models.Model):
    name = models.CharField(max_length=240)
    over_price_money = models.FloatField(default=0)
    over_price_percent = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    celling_start = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class BigCompany (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


UNIQUE_ARRAY_FIELDS = ('barcode',)


class MyManager(models.Manager):
    def prevent_duplicates_in_array_fields(self, model, array_field):
        def duplicate_check(_lookup_params):
            fields = self.model._meta.get_fields()
            for unique_field in UNIQUE_ARRAY_FIELDS:
                unique_field_index = [
                    getattr(field, 'name', '') for field in fields]
                try:
                    # if model doesn't have the unique field, then proceed to the next loop iteration
                    unique_field_index = unique_field_index.index(unique_field)
                except ValueError:
                    continue
            all_items_in_db = [item for sublist in self.values_list(
                fields[unique_field_index].name).exclude(**_lookup_params) for item in sublist]
            all_items_in_db = [
                item for sublist in all_items_in_db for item in sublist]
            if not set(array_field).isdisjoint(all_items_in_db):
                raise ValidationError(
                    '{} contains items already in the database'.format(array_field))
        if model.id:
            lookup_params = {'id': model.id}
        else:
            lookup_params = {}
        duplicate_check(lookup_params)


class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = ArrayField(models.CharField(
        max_length=400, blank=True, null=True), null=True, blank=True, default=list)
    # barcode = models.CharField(max_length=255, null=True, blank=True, unique=True)
    barcode = ArrayField(
        models.CharField(max_length=255, null=True, blank=True), default=list, blank=True, null=True
    )
    no_pocket = models.FloatField(null=True, blank=True)
    no_box = models.FloatField(null=True, default=1)
    pharm_group = models.ForeignKey(
        PharmGroup, on_delete=models.RESTRICT, null=True, blank=True)
    kind = models.ForeignKey(
        Kind, on_delete=models.RESTRICT, null=True, blank=True)
    ml = models.CharField(max_length=50, null=True, blank=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.DO_NOTHING, null=True, blank=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.RESTRICT, null=True, blank=True)
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
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/medician', optimized_image_output_size=(500, 500),
                                optimized_image_resize_method="cover")
    patient_approved = models.BooleanField(default=False)
    doctor_approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    department = models.ManyToManyField(
        Department, blank=True)
    min_expire_date = models.IntegerField(default=6, blank=True)
    big_company = models.ForeignKey(
        BigCompany, on_delete=models.RESTRICT, blank=True, null=True)
    shorted = models.BooleanField(default=False)
    to_buy = models.BooleanField(default=False)
    unsubmited_existence = models.FloatField(default=0)
    # objects = MyManager()

    def __str__(self):
        return str(self.brand_name)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     Medician.objects.prevent_duplicates_in_array_fields(self, self.barcode)
    #     super().save(*args, **kwargs)


GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female")
)


class PatientName (models.Model):
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


class Prescription (models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.RESTRICT)  # انتخاب بخش فروش
    prescription_number = models.CharField(
        max_length=60, unique=True, null=True, blank=True, editable=False)
    name = models.ForeignKey(
        PatientName, on_delete=models.RESTRICT, null=True, blank=True)
    doctor = models.ForeignKey(
        DoctorName, on_delete=models.RESTRICT, null=True, blank=True)
    medician = models.ManyToManyField(Medician, through='PrescriptionThrough')
    grand_total = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    zakat = models.FloatField(default=0)
    khairat = models.FloatField(default=0)
    created = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    rounded_number = models.FloatField(default=0)
    image = OptimizedImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/prescriptions')
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    refund = models.FloatField(default=0)
    barcode = models.ImageField(
        upload_to='frontend/public/dist/images/prescriptions/barcodes', blank=True, editable=False)
    barcode_str = models.CharField(max_length=255, blank=True, editable=False)

    def __str__(self):
        return self.prescription_number

    def save(self, *args, **kwargs):

        objects_count = Prescription.objects.all().count()
        if Prescription.objects.filter(created=date.today()):
            objects_count = Prescription.objects.filter(
                created=date.today()).count()
            new_number = objects_count + 1
        else:
            new_number = "1"
        time = date.today().strftime("%y-%m-%d")
        if self.prescription_number:
            pass
        else:
            self.prescription_number = str(time) + "-" + str(new_number)

        if (self.barcode_str == ''):
            number = random.randint(1000000000000, 9999999999999)
            EAN = barcode.get_barcode_class('upc')
            ean = EAN(f'{number}', writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.barcode_str = ean.get_fullcode()
            self.barcode.save(f'{number}' + '.png', File(buffer), save=False)

        return super().save(*args, **kwargs)


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
        """ Calculation of Total Price for total_price field """

        self.total_price = round(self.quantity * self.each_price, 1)

        super(PrescriptionThrough, self).save(*args, **kwargs)

        def priscription_sum():

            entrance_sum_query = list(EntranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]
            prescription_sum_query = list(PrescriptionThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('quantity')).values())[0]
            outrance_sum_query = list(OutranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]

            if prescription_sum_query and entrance_sum_query == None and outrance_sum_query == None:
                result = -(self.quantity)
            if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
                result = entrance_sum_query - outrance_sum_query
            if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
                result = entrance_sum_query - prescription_sum_query
            if entrance_sum_query == None and prescription_sum_query and outrance_sum_query:
                result = -(prescription_sum_query + outrance_sum_query)
            if prescription_sum_query and entrance_sum_query and outrance_sum_query:
                result = entrance_sum_query - \
                    (prescription_sum_query + outrance_sum_query)
            return result

        self.medician.existence = priscription_sum()
        self.medician.save()

        prescription_through_total = list(PrescriptionThrough.objects.filter(
            prescription_id=self.prescription.id).aggregate(Sum('total_price')
                                                            ).values())[0]

        last_revenue = list(RevenueTrough.objects.filter(
            prescription_id=self.prescription.id).aggregate(Sum('purchased')
                                                            ).values())[0]

        if (self.prescription.sold == True and last_revenue):
            self.prescription.sold = False
            self.prescription.refund = prescription_through_total - last_revenue
        if (self.prescription.sold == True):
            self.prescription.sold = False
        if prescription_through_total:
            self.prescription.grand_total = prescription_through_total
        else:
            self.prescription.grand_total = 0

        if (last_revenue == prescription_through_total):
            self.prescription.sold = True

        self.prescription.save()


class City (models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Market (models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PharmCompany (models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=50, null=True, blank=True)
    ceo_phone = models.IntegerField(null=True, blank=True)
    manager = models.CharField(max_length=50, null=True, blank=True)
    manager_phone = models.IntegerField(null=True, blank=True)
    visitor = models.CharField(max_length=50, null=True, blank=True)
    visitor_phone = models.IntegerField(null=True, blank=True)
    companies = ArrayField(models.CharField(
        max_length=30, null=True, blank=True), null=True, blank=True)
    company_phone_1 = models.IntegerField(null=True,  blank=True)
    company_phone_2 = models.IntegerField(null=True, blank=True)
    company_online = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.RESTRICT, null=True, blank=True)
    market = models.ForeignKey(
        Market, on_delete=models.RESTRICT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Currency (models.Model):
    name = models.CharField(max_length=20)
    rate = models.FloatField()
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Store (models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    responsible = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, default="",
                             upload_to='frontend/public/dist/images/stores')
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PaymentMethod (models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class FinalRegister (models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


WHOLESALE_CHOICE = (
    ("WHOLESALE", "WHOLESALE"),
    ("SINGULAR", "SINGULAR")
)


class Entrance (models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.RESTRICT)
    factor_number = models.IntegerField(null=True, blank=True)
    medicians = models.ManyToManyField(Medician, through='EntranceThrough')
    factor_date = models.DateTimeField(default=timezone.now)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.RESTRICT)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    total_interest = models.IntegerField()
    final_register = models.ForeignKey(
        FinalRegister, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    deliver_by = models.CharField(max_length=100, null=True, blank=True)
    recived_by = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    without_discount = models.BooleanField(default=False)
    discount_percent = models.FloatField(default=0)
    wholesale = models.CharField(
        max_length=100, choices=WHOLESALE_CHOICE, default=1)
    image = OptimizedImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/entrances')
    currency_rate = models.FloatField(default=1)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs):
        self.currency_rate = self.currency.rate

        super(Entrance, self).save(*args, **kwargs)


class EntranceThrough(models.Model):
    entrance = models.ForeignKey(Entrance, on_delete=models.RESTRICT)
    medician = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    number_in_factor = models.IntegerField()
    each_price_factor = models.FloatField()
    each_price = models.FloatField(default=1)
    discount_money = models.FloatField(default=0)
    no_box = models.FloatField(default=1)
    discount_percent = models.FloatField(default=0)
    total_purchaseـafghani = models.FloatField(
        default=1)
    total_purchaseـcurrency = models.FloatField(
        default=1)
    total_purchase_currency_before = models.FloatField(default=0)
    discount_value = models.FloatField(default=0)
    each_quantity = models.FloatField(default=1)
    quantity_bonus = models.FloatField(default=0)
    bonus_value = models.FloatField(default=0)
    shortage = models.FloatField(default=0)
    lease = models.BooleanField(default=False)
    each_purchase_price = models.FloatField(
        default=1)
    each_sell_price = models.FloatField(
        default=0)
    each_sell_price_afg = models.FloatField(
        default=0
    )
    total_sell = models.FloatField(default=0)
    interest_percent = models.FloatField(default=20)
    register_quantity = models.IntegerField(
        default=0)
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

        round_digit = 1

        self.total_purchase_currency_before = round(
            self.number_in_factor * self.each_price_factor, round_digit)
        self.total_purchaseـcurrency = round(self.total_purchase_currency_before * (
            1-self.discount_percent / 100) - self.discount_money, round_digit)
        self.discount_value = round(
            self.total_purchase_currency_before - self.total_purchaseـcurrency, round_digit)
        if (self.quantity_bonus > 0):
            self.bonus_value = round((self.total_purchase_currency_before / (
                self.number_in_factor + self.quantity_bonus)) * self.quantity_bonus, round_digit)
        else:
            self.bonus_value = 0
        self.each_purchase_price = round(
            (self.each_price_factor / self.no_box), round_digit)
        self.each_price = round(
            self.each_purchase_price * (1 + self.interest_percent / 100), round_digit)
        self.total_sell = round(
            self.each_price * self.no_box * self.number_in_factor, round_digit)
        self.register_quantity = ((self.number_in_factor * self.no_box) -
                                  (self.shortage * self.no_box)) + self.quantity_bonus
        self.each_sell_price = round(
            self.each_sell_price_afg / self.entrance.currency_rate, round_digit)
        self.rate = self.entrance.currency_rate
        self.rate_name = self.entrance.currency.name

        self.medician.last_purchased = self.each_purchase_price
        self.medician.save()

        super(EntranceThrough, self).save(*args, **kwargs)

        def entrance_sum():

            entrance_sum_query = list(EntranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]
            prescription_sum_query = list(PrescriptionThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('quantity')).values())[0]
            outrance_sum_query = list(OutranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]

            if entrance_sum_query and prescription_sum_query == None and outrance_sum_query == None:
                result = entrance_sum_query
            if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
                result = entrance_sum_query - outrance_sum_query
            if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
                result = entrance_sum_query - prescription_sum_query
            if entrance_sum_query == None:
                result = -(prescription_sum_query + outrance_sum_query)
            if prescription_sum_query and entrance_sum_query and outrance_sum_query:
                result = entrance_sum_query - \
                    (prescription_sum_query + outrance_sum_query)
            if entrance_sum_query:
                result = entrance_sum_query
            return result

        self.medician.existence = entrance_sum()
        if (entrance_sum() >= self.medician.unsubmited_existence):
            self.medician.unsubmited_existence = 0
        self.medician.save()


class Outrance (models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.CASCADE)
    factor_number = models.IntegerField()
    medicians = models.ManyToManyField(Medician, through='OutranceThrough')
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


class OutranceThrough (models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    outrance = models.ForeignKey(Outrance, on_delete=models.CASCADE)
    number_in_factor = models.IntegerField()  # G4 تعداد در فاکتور
    each_price_factor = models.FloatField()  # G8 قیمت فی خرید توسط کاربر
    each_price = models.FloatField(default=1)  # G5 قیمت فی خرید فاکتور
    discount_money = models.FloatField(default=0)  # G6 تخفیف خرید پولی
    discount_percent = models.FloatField(default=0)  # G7 تخفیف خرید فیصدی
    total_purchaseـafghani = models.FloatField(
        default=1)  # G9 مجموع خرید افغانی
    total_purchaseـcurrency = models.FloatField(
        default=1)  # G10 مجموع خرید اسعاری
    each_quantity = models.IntegerField(default=1)  # G11  تعداد در فی فروش
    bonus = models.IntegerField(default=0)  # G12 بونوس
    quantity_bonus = models.IntegerField(default=0)  # G13 تعداد بیشتر از خرید
    register_quantity = models.IntegerField(
        default=0)  # G14 تعداد ثبت به سیستم جهت موجودی
    each_purchase_price = models.FloatField(
        default=1)  # G18 قیمت فی خرید جهت ثبت به سیستم
    interest_money = models.FloatField(default=0)  # G19 فایده پولی
    interest_percent = models.FloatField(default=20)  # G20 فایده فیصدی
    each_sell_price = models.FloatField(
        default=0)  # G21 قیمت فی فروش جهت ثبت به سیستم
    total_sell = models.FloatField(default=0)  # G25 مجموع فروش
    bonus_interest = models.FloatField(default=0)  # G27 مجموع فروش بونوس دار
    total_interest = models.FloatField(default=0)  # G30 مجموع فایده
    expire_date = models.DateField()  # G31 تاریخ انقضا
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.medician.brand_name + " - " + self.outrance.company.name + ".co"

    def save(self, *args, **kwargs):

        round_digit = 1
        super(OutranceThrough, self).save(*args, **kwargs)

        def entrance_sum():

            entrance_sum_query = list(EntranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]
            prescription_sum_query = list(PrescriptionThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('quantity')).values())[0]
            outrance_sum_query = list(OutranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]

            if entrance_sum_query == None and prescription_sum_query == None:
                result = -(self.register_quantity)
            if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
                result = entrance_sum_query - outrance_sum_query
            if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
                result = entrance_sum_query - prescription_sum_query
            if entrance_sum_query == None and outrance_sum_query and prescription_sum_query:
                result = -(prescription_sum_query + outrance_sum_query)
            if prescription_sum_query and entrance_sum_query and outrance_sum_query:
                result = entrance_sum_query - \
                    (prescription_sum_query + outrance_sum_query)
            return result

        self.medician.existence = entrance_sum()
        self.medician.save()


@receiver(post_delete, sender=OutranceThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):
    entrance_sum_query = list(EntranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]
    prescription_sum_query = list(PrescriptionThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('quantity')).values())[0]
    outrance_sum_query = list(OutranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]

    if entrance_sum_query == None and prescription_sum_query == None and outrance_sum_query == None:
        result = 0
    if prescription_sum_query and entrance_sum_query == None and outrance_sum_query == None:
        result = -(prescription_sum_query)
    if entrance_sum_query and prescription_sum_query == None and outrance_sum_query == None:
        result = entrance_sum_query
    if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
        result = entrance_sum_query - outrance_sum_query
    if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
        result = entrance_sum_query - prescription_sum_query
    if entrance_sum_query == None and prescription_sum_query and outrance_sum_query:
        result = -(prescription_sum_query + outrance_sum_query)
    if prescription_sum_query and entrance_sum_query and outrance_sum_query:
        result = entrance_sum_query - \
            (prescription_sum_query + outrance_sum_query)

    instance.medician.existence = result
    instance.medician.save()


@receiver(post_delete, sender=EntranceThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):
    entrance_sum_query = list(EntranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]
    prescription_sum_query = list(PrescriptionThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('quantity')).values())[0]
    outrance_sum_query = list(OutranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]

    if entrance_sum_query == None and prescription_sum_query == None and outrance_sum_query == None:
        result = 0
    if prescription_sum_query and entrance_sum_query == None and outrance_sum_query == None:
        result = -(prescription_sum_query)
    if entrance_sum_query and prescription_sum_query == None and outrance_sum_query == None:
        result = entrance_sum_query
    if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
        result = entrance_sum_query - outrance_sum_query
    if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
        result = entrance_sum_query - prescription_sum_query
    if entrance_sum_query == None and prescription_sum_query and outrance_sum_query:
        result = -(prescription_sum_query + outrance_sum_query)
    if prescription_sum_query and entrance_sum_query and outrance_sum_query:
        result = entrance_sum_query - \
            (prescription_sum_query + outrance_sum_query)
    else:
        result = 0

    instance.medician.existence = result
    instance.medician.save()


@receiver(post_delete, sender=PrescriptionThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):
    entrance_sum_query = list(EntranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]
    prescription_sum_query = list(PrescriptionThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('quantity')).values())[0]
    outrance_sum_query = list(OutranceThrough.objects.filter(
        medician_id=instance.medician.id).aggregate(Sum('register_quantity')).values())[0]

    if entrance_sum_query == None and prescription_sum_query == None and outrance_sum_query == None:
        result = 0
    if entrance_sum_query and prescription_sum_query == None and outrance_sum_query == None:
        result = entrance_sum_query
    if prescription_sum_query == None and outrance_sum_query and entrance_sum_query:
        result = entrance_sum_query - outrance_sum_query
    if outrance_sum_query == None and prescription_sum_query and entrance_sum_query:
        result = entrance_sum_query - prescription_sum_query
    if entrance_sum_query == None and outrance_sum_query and prescription_sum_query:
        result = -(prescription_sum_query + outrance_sum_query)
    if prescription_sum_query and entrance_sum_query and outrance_sum_query:
        result = entrance_sum_query - \
            (prescription_sum_query + outrance_sum_query)
    if prescription_sum_query and entrance_sum_query == None and outrance_sum_query == None:
        result = -(prescription_sum_query)
    else:
        result = instance.medician.existence

    prescription_through_total = list(PrescriptionThrough.objects.filter(
        prescription_id=instance.prescription.id).aggregate(Sum('total_price')
                                                            ).values())[0]

    if prescription_through_total:
        instance.prescription.grand_total = prescription_through_total
        instance.prescription.save()
    else:
        instance.prescription.grand_total = 0
        instance.prescription.save()

    instance.medician.existence = result
    instance.medician.save()


class Revenue (models.Model):
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
        User, on_delete=models.RESTRICT, related_name='employee')
    revenue_through = models.ManyToManyField(
        Prescription, through="RevenueTrough")

    def update_model(self, *args, **kwargs):
        checkifopen = Revenue.objects.filter(employee=self.employee).filter(
            active=True).filter(~Q(id=self.id))
        print(checkifopen)
        if checkifopen:
            raise Exception('There is Already an Open Revenue...')
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


class RevenueTrough (models.Model):
    revenue = models.ForeignKey(Revenue, on_delete=models.DO_NOTHING)
    prescription = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.FloatField(default=0)
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if (self.prescription.refund == 0):
            self.purchased = self.prescription.grand_total
        if (self.prescription.refund != 0):
            self.purchased = self.prescription.refund
            self.prescription.sold = True
            self.prescription.refund = 0

        if self.sold == True:
            self.prescription.sold = True
            self.prescription.save()

        super(RevenueTrough, self).save()

    # class Meta:
    #     unique_together = ('revenue', 'prescription',)


class PurchaseList (models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.DO_NOTHING)
    need_quautity = models.FloatField(default=0)
    company_1 = models.ForeignKey(PharmCompany, on_delete=models.DO_NOTHING)
    price_1 = models.FloatField(default=0)
    bonus_1 = models.FloatField(default=0)
    date_1 = models.DateField()
    company_2 = models.ForeignKey(
        PharmCompany, on_delete=models.DO_NOTHING, related_name="company_2")
    price_2 = models.FloatField(default=0)
    bonus_2 = models.FloatField(default=0)
    date_2 = models.DateField()
    company_3 = models.ForeignKey(
        PharmCompany, on_delete=models.DO_NOTHING, related_name="company_3")
    price_3 = models.FloatField(default=0)
    bonus_3 = models.FloatField(default=0)
    date_3 = models.DateField()
    arrival_quantity = models.FloatField(default=0)
    shortaged = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine.brand_name


class MedicineWith (models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.RESTRICT)
    includes = models.ManyToManyField(Medician, related_name="medicines")

    def __str__(self):
        return self.medicine.brand_name


class MedicineConflict (models.Model):
    medicine_1 = models.ForeignKey(
        Medician, on_delete=models.DO_NOTHING, related_name="medicine_1")
    medicine_2 = models.ForeignKey(Medician, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.medicine_1.brand_name + " vs " + self.medicine_2.brand_name


@receiver(post_delete, sender=PrescriptionThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):

    prescription_through_total = list(PrescriptionThrough.objects.filter(
        prescription_id=instance.prescription.id).aggregate(Sum('total_price')
                                                            ).values())[0]

    last_revenue = list(RevenueTrough.objects.filter(
        prescription_id=instance.prescription.id).aggregate(Sum('purchased')
                                                            ).values())[0]

    # if (instance.prescription.sold == True and last_revenue):
    #     grand_total_price = instance.prescription.grand_total
    if (prescription_through_total and last_revenue):
        instance.prescription.sold = False
        instance.prescription.refund = prescription_through_total - last_revenue
    elif (last_revenue):
        instance.prescription.sold = False
        instance.prescription.refund = - last_revenue
    else:
        instance.prescription.sold = False
        instance.prescription.refund = 0

    instance.prescription.save()


@receiver(post_delete, sender=RevenueTrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):

    prescription_through_total = list(PrescriptionThrough.objects.filter(
        prescription_id=instance.prescription.id).aggregate(Sum('total_price')
                                                            ).values())[0]

    last_revenue = list(RevenueTrough.objects.filter(
        prescription_id=instance.prescription.id).aggregate(Sum('purchased')
                                                            ).values())[0]

    if (prescription_through_total and last_revenue):
        instance.prescription.sold = False
        instance.prescription.refund = prescription_through_total - last_revenue
    elif (last_revenue):
        instance.prescription.sold = False
        instance.prescription.refund = - last_revenue
    else:
        instance.prescription.sold = False
        instance.prescription.refund = 0

    instance.prescription.save()

    def total_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('purchased')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('purchased')).values())[0]
        else:
            total_revenue_through = 0
        return total_revenue_through

    def discount_revenue_through():
        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__discount_money')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__discount_money')).values())[0]
        else:
            total_revenue_through = 0
        return total_revenue_through

    def khairat_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__khairat')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__khairat')).values())[0]
        else:
            total_revenue_through = 0
        return total_revenue_through

    def zakat_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__zakat')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__zakat')).values())[0]
        else:
            total_revenue_through = 0
        return total_revenue_through

    def rounded_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__rounded_number')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__rounded_number')).values())[0]
        else:
            total_revenue_through = 0
        return total_revenue_through

    instance.revenue.rounded = rounded_revenue_through()
    instance.revenue.zakat = zakat_revenue_through()
    instance.revenue.khairat = khairat_revenue_through()
    instance.revenue.discount = discount_revenue_through()
    instance.revenue.total = total_revenue_through()
    instance.revenue.save()


@receiver(post_save, sender=RevenueTrough)
def revenue_through_submit(sender, instance, **kwargs):

    def total_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('purchased')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('purchased')).values())[0]
        else:
            total_revenue_through = instance.prescription.grand_total
        return total_revenue_through

    def discount_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__discount_money')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__discount_money')).values())[0]
        else:
            total_revenue_through = instance.prescription.discount_money
        return total_revenue_through

    def khairat_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__khairat')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__khairat')).values())[0]
        else:
            total_revenue_through = instance.prescription.khairat
        return total_revenue_through

    def zakat_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__zakat')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__zakat')).values())[0]
        else:
            total_revenue_through = instance.prescription.zakat
        return total_revenue_through

    def rounded_revenue_through():

        total_revenue_through = list(RevenueTrough.objects.filter(
            revenue_id=instance.revenue.id).aggregate(Sum('prescription__rounded_number')).values())[0]
        if total_revenue_through != None:
            total_revenue_through = list(RevenueTrough.objects.filter(
                revenue_id=instance.revenue.id).aggregate(Sum('prescription__rounded_number')).values())[0]
        else:
            total_revenue_through = instance.prescription.rounded_number
        return total_revenue_through

    instance.revenue.rounded = rounded_revenue_through()
    instance.revenue.zakat = zakat_revenue_through()
    instance.revenue.khairat = khairat_revenue_through()
    instance.revenue.discount = discount_revenue_through()
    instance.revenue.total = total_revenue_through()
    instance.revenue.save()


class PurchaseListManual (models.Model):
    medicine = models.ForeignKey(Medician, on_delete=models.CASCADE)
    quantity = models.FloatField()
    arrival = models.FloatField(default=0)
    approved = models.BooleanField(default=False)
    shortaged = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.medicine.brand_name

    def update_model(self, *args, **kwargs):
        queryset = PurchaseListManual.objects.filter(approved=False).filter(
            medicine=self.medicine).filter(~Q(id=self.id))
        if queryset:
            raise Exception("This Item is Already Set.")
        else:
            super(PurchaseListManual, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if (self.arrival > 0):
            self.approved = True
            self.medicine.unsubmited_existence = self.arrival
            self.medicine.save()
        if (self.arrival == 0):
            self.approved = False
            self.medicine.unsubmited_existence = self.arrival
            self.medicine.save()
        self.update_model()
