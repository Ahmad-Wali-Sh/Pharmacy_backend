from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum


class Kind(models.Model):
    name = models.CharField(max_length=60)
    image = models.FileField(
        null=True, blank=True, default="", upload_to='frontend/public/dist/images/kinds')

    def __str__(self):
        return self.name


class PharmGroup(models.Model):
    name = models.CharField(max_length=60)
    image = models.FileField(null=True, blank=True, default="",
                             upload_to='frontend/public/dist/images/pharm_groub')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(null=True, blank=True, default="",
                             upload_to='frontend/public/dist/images/countries')

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = ArrayField(models.CharField(
        max_length=100, blank=True, null=True))
    no_pocket = models.IntegerField(null=True, blank=True)
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
    barcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    existence = models.IntegerField(default=0, null=True)
    minmum_existence = models.FloatField()
    maximum_existence = models.FloatField()
    must_advised = models.BooleanField(default=False)
    dividing_rules = models.TextField(blank=True, null=True)
    cautions = models.TextField(blank=True, null=True)
    usages = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, default="",
                             upload_to='frontend/public/dist/images/medician')

    def __str__(self):
        return self.brand_name


class Department (models.Model):
    name = models.CharField(max_length=240)
    over_price_money = models.FloatField(default=0)
    over_price_percent = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PersonalName (models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class DoctorName(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Prescription (models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE)  # انتخاب بخش فروش
    prescription_number = models.CharField(max_length=60, unique=True)
    name = models.ForeignKey(
        PersonalName, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(
        DoctorName, on_delete=models.CASCADE, null=True, blank=True)
    medician = models.ManyToManyField(Medician, through='PrescriptionThrough')
    grand_total = models.FloatField(default=0)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    zakat = models.FloatField(default=0)
    khairat = models.FloatField(default=0)

    def __str__(self):
        return self.prescription_number


class PrescriptionThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    each_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

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

            if prescription_sum_query == None:
                result = entrance_sum_query
            else:
                result = entrance_sum_query - prescription_sum_query
            return result

        self.medician.existence = priscription_sum()
        self.medician.save()


class PharmCompany (models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=50)
    ceo_phone = models.IntegerField(null=True, blank=True)
    manager = models.CharField(max_length=50)
    manager_phone = models.IntegerField(null=True, blank=True)
    visitor = models.CharField(max_length=50)
    visitor_phone = models.IntegerField(null=True, blank=True)
    companies = ArrayField(models.CharField(max_length=100))
    company_phone_1 = models.IntegerField()
    company_phone_2 = models.IntegerField(null=True, blank=True)
    company_online = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150)
    description = models.TextField()

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
    address = models.CharField(max_length=200)
    rsponsible = models.CharField(max_length=100)
    description = models.TextField()
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


class Entrance (models.Model):
    company = models.ForeignKey(PharmCompany, on_delete=models.CASCADE)
    factor_number = models.IntegerField()
    medicians = models.ManyToManyField(Medician, through='EntranceThrough')
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

    def __str__(self):
        return self.medician.brand_name + " - " + self.entrance.company.name + ".co"

    def save(self, *args, **kwargs):

        round_digit = 1

        """ محاسبه قیمت فی خرید فاکتور"""

        self.each_price = round(- \
            (self.discount_money-(self.each_price_factor *
             (1-self.discount_percent / 100))) * self.entrance.currency.rate, round_digit)

 
        """   محاسبه مجموع خرید"""

        self.total_purchaseـafghani = round(self.each_price * self.number_in_factor, round_digit)
        self.total_purchaseـcurrency = round(self.each_price_factor * self.number_in_factor, round_digit)

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
            self.each_purchase_price = round(bonus_each_purchase_price + \
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
            self.total_sell = round(bonus_total_sell + quantity_bonus_total_sell, round_digit)

        """ محاسبه فایده """

        quantity_bonus_interest = (
            quantity_bonus_total_sell - self.total_purchaseـafghani) * self.quantity_bonus  # G28
        dicount_interest = (self.each_price_factor *
                            self.entrance.currency.rate)-self.each_price  # G29

        if quantity_bonus_interest == 0:
            simple_interest = simple_total_sell - self.total_purchaseـafghani
        else:
            simple_interest = 0  # G26

        self.total_interest = round(simple_interest + self.bonus_interest + \
            quantity_bonus_interest + dicount_interest, round_digit) # G30

       

        super(EntranceThrough, self).save(*args, **kwargs)

        def entrance_sum():

            entrance_sum_query = list(EntranceThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('register_quantity')).values())[0]
            prescription_sum_query = list(PrescriptionThrough.objects.filter(
                medician_id=self.medician.id).aggregate(Sum('quantity')).values())[0]

            if prescription_sum_query == None:
                result = entrance_sum_query
            else:
                result = entrance_sum_query - prescription_sum_query
            return result

        self.medician.existence = entrance_sum()
        self.medician.save()
