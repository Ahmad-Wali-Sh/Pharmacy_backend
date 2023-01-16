from django.db import models
from medician.models import Medician

class Prescription (models.Model):
    name = models.CharField(max_length=80)
    code = models.IntegerField()
    medician = models.ManyToManyField(Medician)
    prescription_number = models.CharField(max_length=60)

    def __str__(self):
        return self.name
