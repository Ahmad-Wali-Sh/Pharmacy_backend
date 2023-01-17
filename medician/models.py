from django.db import models

class Kind(models.Model):
    name = models.CharField(max_length=60)

    def __str__ (self):
        return self.name

class Pharm_Group(models.Model):
    name = models.CharField(max_length=60)

    def __str__ (self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__ (self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=5)

    def __str__ (self):
        return self.name

class Medician(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100, blank=True, null=True)
    no_pocket = models.IntegerField()
    pharm_group = models.ForeignKey(Pharm_Group, on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)
    ml = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    minmum_existence = models.FloatField()
    maximum_existence = models.FloatField()
    dividing_rules = models.TextField(blank=True, null=True)
    cautions = models.TextField(blank=True, null=True)
    usages = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, default="", upload_to='D:/Personaly/Pharmacy App/Pharmacy_app/backend/frontend/public/images')

    def __str__ (self):
        return self.brand_name




