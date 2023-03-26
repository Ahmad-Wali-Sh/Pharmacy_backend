from django.db import models
from django.contrib.postgres.fields import ArrayField


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
    # need array field
    generic_name = models.CharField(max_length=100, blank=True, null=True)
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
    existence = models.IntegerField(default=0)
    minmum_existence = models.FloatField()
    maximum_existence = models.FloatField()
    dividing_rules = models.TextField(blank=True, null=True)
    cautions = models.TextField(blank=True, null=True)
    usages = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, default="",
                             upload_to='frontend/public/dist/images/medician')

    def __str__(self):
        return self.brand_name


class Prescription (models.Model):
    name = models.CharField(max_length=80)
    code = models.IntegerField()
    medician = models.ManyToManyField(Medician)
    prescription_number = models.CharField(max_length=60)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.company.name


class EntranceThrough(models.Model):
    medician = models.ForeignKey(Medician, on_delete=models.CASCADE)
    entrance = models.ForeignKey(Entrance, on_delete=models.CASCADE)
    # تعداد در فاکتور
    number_in_factor = models.IntegerField()
    each_price_factor = models.FloatField(default=0)
    each_price = models.FloatField(default=1)
    discount_money = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    total_purchase = models.FloatField(default=1)  # مجموع خرید
    each_quantity = models.IntegerField(default=1)  # تعداد در فی فروش
    bonus = models.IntegerField(default=0)  # بونوس
    quantity_bonus = models.IntegerField(default=0)  # تعداد بیشتر از خرید
    register_quantity = models.IntegerField(
        default=0)  # تعداد ثبت به سیستم جهت موجودی
    each_purchase_price = models.FloatField(
        default=1)  # قیمت فی خرید جهت ثبت به سیستم
    interest_money = models.FloatField(default=0)  # فایده پولی
    interest_percent = models.FloatField(default=20)  # فایده فیصدی
    each_sell_price = models.FloatField(
        default=0)  # قیمت فی فروش جهت ثبت به سیستم
    total_sell = models.FloatField(default=0)  # مجموع فروش
    bonus_interest = models.FloatField(default=0)
    total_interest = models.FloatField(default=0)  # مجموع فایده
    expire_date = models.DateField()  # تاریخ انقضا

    def __str__(self):
        return self.medician.brand_name + " from " + self.entrance.company.name

    def save(self, *args, **kwargs):

        round_digit = 1

        """ Calculation iof currency """

        rated = self.each_price_factor * self.entrance.currency.rate
        self.each_price = rated

        """Calculation of discounts for each_price Field"""

        if self.discount_percent != 0:
            self.each_price = rated - \
                ((rated * self.discount_percent) / 100)

        if self.discount_money != 0:
            self.each_price = (
                rated - self.discount_money)

        """ Calculation of total purchase for total_purchase field"""
        if self.total_purchase == 1:
            self.total_purchase = self.total_purchase * \
                rated * self.number_in_factor

        elif self.total_purchase != 1:
            self.total_purchase = (
                self.total_purchase * rated / self.total_purchase) * self.number_in_factor

        """ Calculation of Register Qunatity & Calculation of Medician Existence Incress"""

        self.register_quantity = (
            self.each_quantity * self.number_in_factor) + self.bonus + self.quantity_bonus
        self.medician.existence = self.medician.existence + self.register_quantity
        if self.each_purchase_price == 1:
            self.medician.save()

        """ Calculation of Each Price Purchase for field each_price_purchase """

        simple_each_price = self.total_purchase / \
            (self.number_in_factor * self.each_quantity)
        bonus_each_price = ((rated / (self.number_in_factor *
                            self.each_quantity)) * self.number_in_factor) * self.bonus
        bonus_quantity_each_price = (self.total_purchase / (
            (self.number_in_factor * self.each_quantity) + self.quantity_bonus)) * self.quantity_bonus

        if self.bonus == 0 and self.quantity_bonus == 0:
            self.each_purchase_price = round(simple_each_price, round_digit)
        else:
            self.each_purchase_price = round(
                (bonus_each_price + bonus_quantity_each_price), round_digit)

        """ Calculation of Each Sell Price for each_sell_price field """

        self.each_sell_price = round(
            (self.interest_money + (self.each_purchase_price*(1 + (self.interest_percent / 100)))), round_digit)

        """ Calculation of Total Sell for total_sell field """
        self.total_sell = round(
            self.each_sell_price * self.register_quantity, round_digit)

        """ Calculation of Bonus Interest for bonus_interset field """
        self.bonus_interest = round(self.bonus * bonus_each_price, round_digit)

        """ Calculation of Total Interset of interest field """
        interest = round(self.total_sell - self.total_purchase, round_digit)
        self.total_interest = round(
            self.bonus_interest + interest, round_digit)

        super(EntranceThrough, self).save(*args, **kwargs)
