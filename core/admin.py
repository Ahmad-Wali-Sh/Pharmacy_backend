from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, OutranceThrough, \
        Outrance, City, Market, Revenue, MedicineBarcode, RevenueTrough, EntranceImage, MedicineWith, BigCompany, MedicineConflict, PurchaseList, PurchaseListManual

from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

from django.contrib.auth.admin import UserAdmin
from .models import User 


UserAdmin.list_display += ('image',)
UserAdmin.list_filter += ('image',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('image', )}),)


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    skip_admin_log = True
    IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = False
    pass 

class EntracnceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = (
        ('factor_date', JDateFieldListFilter),
    )

class MedicineImport(resources.ModelResource):
    kind = fields.Field(
        column_name='kind',
        attribute='name_persian',
        widget=ForeignKeyWidget(Kind, 'name_persian')
    )
    big_company = fields.Field(
        column_name='big_company',
        attribute='big_company',
        widget=ForeignKeyWidget(BigCompany, 'name')
    )
    pharm_group = fields.Field(
        column_name='pharm_group',
        attribute='pharm_group',
        widget=ForeignKeyWidget(PharmGroup, 'name_english')
    )
    country = fields.Field(
        column_name='country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'name')
    )

    class Meta:
        model = Medician

    # def save_instance(self, instance, using_transactions=True, dry_run=False, *args, **kwargs):
    #     if (instance.kind):
    #         kind_name = instance.kind
    #         try:
    #             # Try to get the related Kind object by name_persian
    #             kind = Kind.objects.get(name_persian=kind_name)
    #         except Kind.DoesNotExist:
    #             # If Kind does not exist, create a new one
    #             admin_user = User.objects.get(username="admin")
    #             kind = Kind(name_persian=kind_name, user=admin_user)
    #             kind.save()
    #         instance.kind = kind    

    #     return super().save_instance(instance, using_transactions=using_transactions, dry_run=dry_run, *args, **kwargs)

    # def before_import_row(self, row, **kwargs):
    #     if ('kind' in row):
    #         kind_name = row['kind']
    #         try:
    #             Kind.objects.get(name_persian=kind_name)
    #         except Kind.DoesNotExist:
    #             admin_user = User.objects.get(username="admin")
    #             Kind.objects.create(name_persian=kind_name, user=admin_user)
    #     else: pass

class EntranceThrougheAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('register_quantity', 'each_purchase_price', 'total_sell', 'bonus_interest', 'total_purchaseـafghani', 
                       'total_purchaseـcurrency','total_interest', 'each_price', 'total_purchase_currency_before', 'discount_value', 'each_quantity', 'bonus_value', 'each_sell_price', 'interest_money')


class PrescriptionThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('total_price' ,)

class MedicineAdmin(ImportExportModelAdmin):
    resource_class = MedicineImport

admin.site.register(User, UserAdmin)
admin.site.register(PharmGroup, ImportAdmin)
admin.site.register(Medician, MedicineAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(Prescription, ImportAdmin)
admin.site.register(PharmCompany, ImportAdmin)
admin.site.register(Entrance, EntracnceAdmin)
admin.site.register(MedicineBarcode, ImportAdmin)
admin.site.register(Store, ImportAdmin)
admin.site.register(PurchaseListManual, ImportAdmin)
admin.site.register(EntranceImage, ImportAdmin)
admin.site.register(MedicineWith, ImportAdmin)
admin.site.register(Currency, ImportAdmin)
admin.site.register(EntranceThrough, EntranceThrougheAdmin)
admin.site.register(PaymentMethod, ImportAdmin)
admin.site.register(FinalRegister, ImportAdmin)
admin.site.register(Department, ImportAdmin)
admin.site.register(Outrance, ImportAdmin)
admin.site.register(OutranceThrough, ImportAdmin)
admin.site.register(BigCompany, ImportAdmin)
admin.site.register(DoctorName, ImportAdmin)
admin.site.register(City, ImportAdmin)
admin.site.register(PurchaseList, ImportAdmin)
admin.site.register(Market, ImportAdmin)
admin.site.register(PatientName, ImportAdmin)
admin.site.register(Revenue, ImportAdmin)
admin.site.register(RevenueTrough, ImportAdmin)
admin.site.register(MedicineConflict, ImportAdmin)
admin.site.register(PrescriptionThrough, PrescriptionThroughAdmin)

# Register your models here.
