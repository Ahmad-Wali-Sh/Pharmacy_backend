from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from image_optimizer.fields import OptimizedImageField
from datetime import date
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

from django.utils import timezone
from django.db.models.signals import post_delete, pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _, ngettext_lazy
from django import forms
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError


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
    name_english = models.CharField(max_length=60, null=True, blank=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/kinds')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_english


class PharmGroup(models.Model):
    name_english = models.CharField(max_length=60, null=True, blank=True)
    name_persian = models.CharField(max_length=60, null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/pharm_groub')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_english


class Country(models.Model):
    name = models.CharField(max_length=50)
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/countries')

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

# UNIQUE_ARRAY_FIELDS = ('name','barcode',)

# class MyManager(models.Manager):
#     def prevent_duplicates_in_array_fields(self, model, array_field):
#         def duplicate_check(_lookup_params):
#             fields = self.model._meta.get_fields()
#             for unique_field in UNIQUE_ARRAY_FIELDS:
#                 unique_field_index = [getattr(field, 'name', 'barcode') for field in fields]
#                 try:
#                     # if model doesn't have the unique field, then proceed to the next loop iteration
#                     unique_field_index = unique_field_index.index(unique_field)
#                 except ValueError:
#                     continue
#             all_items_in_db = [item for sublist in self.values_list(fields[unique_field_index].name).exclude(**_lookup_params) for item in sublist]
#             all_items_in_db = [item for sublist in all_items_in_db for item in sublist]
#             if not set(array_field).isdisjoint(all_items_in_db):
#                 raise ValidationError('{} contains items already in the database'.format(array_field))
#         if model.id:
#             lookup_params = {'id': model.id}
#         else:
#             lookup_params = {}
#         duplicate_check(lookup_params)


class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = ArrayField(models.CharField(
        max_length=100, blank=True, null=True), null=True, blank=True, default=list)
    # barcode = ArrayField(models.CharField(
    #     max_length=200, blank=True, null=True, unique=True), default=list,null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    no_pocket = models.FloatField(null=True, blank=True)
    no_box = models.FloatField(null=True, blank=True)
    pharm_group = models.ForeignKey(
        PharmGroup, on_delete=models.CASCADE, null=True, blank=True)
    kind = models.ForeignKey(
        Kind, on_delete=models.CASCADE, null=True, blank=True)
    ml = models.CharField(max_length=50, null=True, blank=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    existence = models.FloatField(default=0, null=True)
    minmum_existence = models.FloatField()
    maximum_existence = models.FloatField()
    must_advised = models.BooleanField(default=False)
    dividing_rules = models.TextField(blank=True, null=True)
    cautions = models.TextField(blank=True, null=True)
    usages = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = OptimizedImageField(null=True, blank=True, default="",
                                upload_to='frontend/public/dist/images/medician')
    patient_approved = models.BooleanField(default=False)
    doctor_approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    

    # objects = MyManager()

    def __str__(self):
        return self.brand_name

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     Medician.objects.prevent_duplicates_in_array_fields(self, self.barcode)
    #     super().save(*args, **kwargs)


class Department (models.Model):
    name = models.CharField(max_length=240)
    over_price_money = models.FloatField(default=0)
    over_price_percent = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    celling_start = models.FloatField(default=0)

    def __str__(self):
        return self.name


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Prescription (models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE)  # انتخاب بخش فروش
    prescription_number = models.CharField(
        max_length=60, unique=True, null=True, blank=True, editable=False)
    name = models.ForeignKey(
        PatientName, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(
        DoctorName, on_delete=models.CASCADE, null=True, blank=True)
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
            super(Prescription, self).save()
        else:
            self.prescription_number = str(time) + "-" + str(new_number)
            super(Prescription, self).save()


class PrescriptionThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    each_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

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

        if prescription_through_total:
            self.prescription.grand_total = prescription_through_total
            self.prescription.save()
        else:
            self.prescription.grand_total = 0
            self.prescription.save()


class City (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Market (models.Model):
    name = models.CharField(max_length=100)

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
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Currency (models.Model):
    name = models.CharField(max_length=20)
    rate = models.FloatField()
    description = models.TextField()

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

    def __str__(self):
        return self.name


class PaymentMethod (models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class FinalRegister (models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

WHOLESALE_CHOICE = (
    ("WHOLESALE", "WHOLESALE"),
    ("SINGULAR", "SINGULAR")
)


class Entrance (models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.CASCADE)
    factor_number = models.IntegerField(null=True, blank=True)
    medicians = models.ManyToManyField(Medician, through='EntranceThrough')
    factor_date = models.DateTimeField(default=timezone.now)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    total_interest = models.IntegerField()
    final_register = models.ForeignKey(FinalRegister, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    deliver_by = models.CharField(max_length=100, null=True, blank=True)
    recived_by = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    without_discount = models.BooleanField(default=False)
    wholesale = models.CharField(max_length=100, choices=WHOLESALE_CHOICE, default=1)
    image = OptimizedImageField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/entrances')

    def __str__(self):
        return self.company.name


class EntranceThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    entrance = models.ForeignKey(Entrance, on_delete=models.CASCADE)
    number_in_factor = models.IntegerField()  # G4 تعداد در فاکتور
    each_price_factor = models.FloatField()  # G8 قیمت فی خرید توسط کاربر
    each_price = models.FloatField(default=1)  # G5 قیمت فی خرید فاکتور
    discount_money = models.FloatField(default=0)  # G6 تخفیف خرید پولی
    discount_percent = models.FloatField(default=0)  # G7 تخفیف خرید فیصدی
    total_purchaseـafghani = models.FloatField(
        default=1)  # G9 مجموع خرید افغانی
    total_purchaseـcurrency = models.FloatField(
        default=1)  # G10 مجموع خرید اسعاری
    each_quantity = models.FloatField(default=1)  # G11  تعداد در فی فروش
    no_box = models.FloatField(default=1)
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
    batch_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.medician.brand_name + " - " + self.entrance.company.name + ".co"

    def save(self, *args, **kwargs):

        round_digit = 1

        """ محاسبه قیمت فی خرید فاکتور"""

        self.each_price = round(-
                                (self.discount_money-(self.each_price_factor *
                                                      (1-self.discount_percent / 100))) * self.entrance.currency.rate, round_digit)
        """
        discount_money = تخیف پولی
        discount_percent = تخفیف فیصدی
        total_purchase_afghani = مجموع قیمت خرید به افغانی
        total_purchase_currenry = مجموع قیمت خرید به ارز
        number_in_factor = تعداد در فاکتور
        each_price_factor = قیمت در فاکتور
        each_price = قیمت فی خرید
        register_quantity = تعداد ثبت
        bonus = بونوس
        interest_money = فایده پولی
        interest_percent = فایده فیصدی
        
        
        """

        """   محاسبه مجموع خرید"""

        self.total_purchaseـafghani = round(
            self.each_price * self.number_in_factor, round_digit)
        self.total_purchaseـcurrency = round(
            self.each_price_factor * self.number_in_factor, round_digit)

        """ محاسبه تعداد ثبت به سیستم"""

        self.register_quantity = round((
            self.number_in_factor * self.each_quantity) + self.bonus + self.quantity_bonus, round_digit)

        """ محاسبه قیمت فی خریده"""

        simple_each_purchase = self.total_purchaseـafghani / \
            (self.number_in_factor * self.each_quantity)  # G15


        bonus_each_purchase_price = self.total_purchaseـafghani / ((self.number_in_factor * self.each_quantity) + self.quantity_bonus )
            
        print(self.total_purchaseـafghani)

        quantity_bonus_each_purchase_price = (self.total_purchaseـafghani / (
            (self.number_in_factor) + self.quantity_bonus))  # G17


        if self.bonus == 0 and self.quantity_bonus == 0:
            self.each_purchase_price = round(simple_each_purchase, 1)

        else:
            self.each_purchase_price = round(bonus_each_purchase_price, 1)

        # self.each_purchase_price = (self.total_purchaseـafghani) / (self.number_in_factor + self.quantity_bonus)

        """ محاسبه قیمت فی فروش"""

        self.each_sell_price = round(
            self.interest_money + (self.each_purchase_price * (1 + self.interest_percent / 100)), round_digit)

        self.medician.price = self.each_sell_price
        self.medician.save()

        """ محاسبه مجموع فروش"""

        simple_total_sell = self.each_sell_price * \
            self.each_quantity * self.number_in_factor  # G22
        bonus_total_sell = self.each_sell_price * \
            ((self.each_quantity * self.number_in_factor) +
             self.bonus) * self.bonus  # G23
        quantity_bonus_total_sell = self.each_sell_price * \
            ((self.each_quantity * self.number_in_factor) +
             self.quantity_bonus) # G24

        if bonus_total_sell == 0 and quantity_bonus_total_sell == 0:
            self.total_sell = round(simple_total_sell, round_digit)
        else:
            self.total_sell = round(
                quantity_bonus_total_sell, round_digit)

        """ محاسبه فایده """

        quantity_bonus_interest = (
            quantity_bonus_total_sell - self.total_purchaseـafghani) * self.quantity_bonus  # G28
        dicount_interest = (self.each_price_factor *
                            self.entrance.currency.rate)-self.each_price  # G29

        if quantity_bonus_interest == 0:
            simple_interest = simple_total_sell - self.total_purchaseـafghani
        else:
            simple_interest = 0  # G26

        # Discount Interest on Entrance Without Discount result.

        if self.entrance.without_discount == False:

            self.total_interest = round(simple_interest + self.bonus_interest +
                                        quantity_bonus_interest + dicount_interest, round_digit)  # G30
        else:
            self.total_interest = round(simple_interest + self.bonus_interest +
                                        quantity_bonus_interest, round_digit)

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
            return result

        self.medician.existence = entrance_sum()
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

    def __str__(self):
        return self.medician.brand_name + " - " + self.outrance.company.name + ".co"

    def save(self, *args, **kwargs):

        round_digit = 1

        """ محاسبه قیمت فی خرید فاکتور"""

        self.each_price = round(-
                                (self.discount_money-(self.each_price_factor *
                                                      (1-self.discount_percent / 100))) * self.outrance.currency.rate, round_digit)

        """   محاسبه مجموع خرید"""

        self.total_purchaseـafghani = round(
            self.each_price * self.number_in_factor, round_digit)
        self.total_purchaseـcurrency = round(
            self.each_price_factor * self.number_in_factor, round_digit)

        """ محاسبه تعداد ثبت به سیستم"""

        self.register_quantity = round((
            self.number_in_factor * self.each_quantity) + self.bonus + self.quantity_bonus, round_digit)

        """ محاسبه قیمت فی خریده"""

        simple_each_purchase = self.total_purchaseـafghani / \
            (self.number_in_factor * self.each_quantity)  # G15
        bonus_each_purchase_price = (
            (self.each_price / (self.number_in_factor * self.each_quantity)) * self.number_in_factor)*self.bonus  # G16
        quantity_bonus_each_purchase_price = (self.total_purchaseـafghani / (
            (self.number_in_factor * self.each_quantity) + self.quantity_bonus))*self.quantity_bonus  # G17
        if self.bonus == 0 and self.quantity_bonus == 0:
            self.each_purchase_price = round(simple_each_purchase, round_digit)
        else:
            self.each_purchase_price = round(bonus_each_purchase_price +
                                             quantity_bonus_each_purchase_price, round_digit)

        """ محاسبه قیمت فی فروش"""

        self.each_sell_price = round(
            self.interest_money + (self.each_purchase_price * (1 + self.interest_percent / 100)), round_digit)

        """ محاسبه مجموع فروش"""

        simple_total_sell = self.each_sell_price * \
            self.each_quantity * self.number_in_factor  # G22
        bonus_total_sell = self.each_sell_price * \
            ((self.each_quantity * self.number_in_factor) +
             self.bonus) * self.bonus  # G23
        quantity_bonus_total_sell = self.each_sell_price * \
            ((self.each_quantity * self.number_in_factor) +
             self.quantity_bonus) * self.quantity_bonus  # G24

        if bonus_total_sell == 0 and quantity_bonus_total_sell == 0:
            self.total_sell = round(simple_total_sell, round_digit)
        else:
            self.total_sell = round(
                bonus_total_sell + quantity_bonus_total_sell, round_digit)

        """ محاسبه فایده """

        quantity_bonus_interest = (
            quantity_bonus_total_sell - self.total_purchaseـafghani) * self.quantity_bonus  # G28
        dicount_interest = (self.each_price_factor *
                            self.outrance.currency.rate)-self.each_price  # G29

        if quantity_bonus_interest == 0:
            simple_interest = simple_total_sell - self.total_purchaseـafghani
        else:
            simple_interest = 0  # G26

        # Discount Interest on Entrance Without Discount result.

        if self.outrance.without_discount == False:
            self.total_interest = round(simple_interest + self.bonus_interest +
                                        quantity_bonus_interest + dicount_interest, round_digit)  # G30
        else:
            self.total_interest = round(simple_interest + self.bonus_interest +
                                        quantity_bonus_interest, round_digit)

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
    active = models.BooleanField(default=True)


class RevenueTrough (models.Model):
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        
        if self.sold == True:
            self.prescription.sold = True
            self.prescription.save()
        super(RevenueTrough, self).save()