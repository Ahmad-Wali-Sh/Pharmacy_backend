from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
<<<<<<< HEAD
    Entrance, Store, Currency, EntranceThroughModel
=======
                        Store, Currency, Entrance, EntranceThrough
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


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
admin.site.register(EntranceThrough, ImportAdmin)

# Register your models here.