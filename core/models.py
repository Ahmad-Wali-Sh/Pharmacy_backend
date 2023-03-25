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


class Entrance (models.Model):
    name = models.CharField(max_length=10, null=True)
    company = models.ForeignKey(
        PharmCompany, on_delete=models.CASCADE, null=True)
    code = models.IntegerField(null=True)
    medicians = models.ManyToManyField(
        Medician, through='EntranceThroughModel')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class EntranceThroughModel(models.Model):
    medician = models.ForeignKey(
        Medician, on_delete=models.CASCADE, null=True)
    entrance = models.ForeignKey(
        Entrance, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(null=True)
    each_price = models.FloatField(null=True)
    total = models.FloatField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
