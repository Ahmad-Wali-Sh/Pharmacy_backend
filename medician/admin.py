from django.contrib import admin

from .models import Pharm_Group, Medician, Kind, Country

admin.site.register(Pharm_Group)
admin.site.register(Medician)
admin.site.register(Kind)
admin.site.register(Country)

# Register your models here.
