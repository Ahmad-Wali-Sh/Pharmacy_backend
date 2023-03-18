from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.models import Pharm_Group, Medician, Kind, Country, Unit, Prescription, PharmCompany


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Pharm_Group, ImportAdmin)
admin.site.register(Medician, ImportAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(Prescription, ImportAdmin)
admin.site.register(PharmCompany, ImportAdmin)

# Register your models here.
