from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, OutranceThrough, \
        Outrance, City, Market, Revenue, RevenueTrough, MedicineWith

from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

from django.contrib.auth.admin import UserAdmin
from .models import User 


UserAdmin.list_display += ('image',)
UserAdmin.list_filter += ('image',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('image', )}),)


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass 

class EntracnceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = (
        ('factor_date', JDateFieldListFilter),
    )


class EntranceThrougheAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('register_quantity', 'each_purchase_price', 'total_sell', 'bonus_interest', 'total_purchaseـafghani', 
                       'total_purchaseـcurrency','total_interest', 'each_price')


class PrescriptionThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('total_price' ,)



admin.site.register(User, UserAdmin)
admin.site.register(PharmGroup, ImportAdmin)
admin.site.register(Medician, ImportAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(Prescription, ImportAdmin)
admin.site.register(PharmCompany, ImportAdmin)
admin.site.register(Entrance, EntracnceAdmin)
admin.site.register(Store, ImportAdmin)
admin.site.register(MedicineWith, ImportAdmin)
admin.site.register(Currency, ImportAdmin)
admin.site.register(EntranceThrough, EntranceThrougheAdmin)
admin.site.register(PaymentMethod, ImportAdmin)
admin.site.register(FinalRegister, ImportAdmin)
admin.site.register(Department, ImportAdmin)
admin.site.register(Outrance, ImportAdmin)
admin.site.register(OutranceThrough, ImportAdmin)
admin.site.register(DoctorName, ImportAdmin)
admin.site.register(City, ImportAdmin)
admin.site.register(Market, ImportAdmin)
admin.site.register(PatientName, ImportAdmin)
admin.site.register(Revenue, ImportAdmin)
admin.site.register(RevenueTrough, ImportAdmin)
admin.site.register(PrescriptionThrough, PrescriptionThroughAdmin)

# Register your models here.
