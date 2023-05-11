from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, OutranceThrough, \
        Outrance


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass 


class EntranceThrougheAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('register_quantity', 'each_purchase_price',
                       'each_sell_price', 'total_sell', 'bonus_interest', 'total_purchaseـafghani', 
                       'total_purchaseـcurrency','total_interest', 'each_price')


class PrescriptionThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('total_price' ,)


admin.site.register(PharmGroup, ImportAdmin)
admin.site.register(Medician, ImportAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(Prescription, ImportAdmin)
admin.site.register(PharmCompany, ImportAdmin)
admin.site.register(Entrance, ImportAdmin)
admin.site.register(Store, ImportAdmin)
admin.site.register(Currency, ImportAdmin)
admin.site.register(EntranceThrough, EntranceThrougheAdmin)
admin.site.register(PaymentMethod, ImportAdmin)
admin.site.register(FinalRegister, ImportAdmin)
admin.site.register(Department, ImportAdmin)
admin.site.register(Outrance, ImportAdmin)
admin.site.register(OutranceThrough, ImportAdmin)
admin.site.register(DoctorName, ImportAdmin)
admin.site.register(PatientName, ImportAdmin)
admin.site.register(PrescriptionThrough, PrescriptionThroughAdmin)

# Register your models here.
