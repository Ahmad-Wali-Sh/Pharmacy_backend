from django.contrib import admin

from .models import Pharm_Group, Prescription, Kind, Country

admin.site.register(Pharm_Group)
admin.site.register(Prescription)
admin.site.register(Kind)
admin.site.register(Country)

# Register your models here.
