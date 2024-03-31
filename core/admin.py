from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from core.models import (
    PharmGroup,
    Medician,
    Kind,
    Country,
    Unit,
    Prescription,
    PharmCompany,
    Store,
    Currency,
    Entrance,
    EntranceThrough,
    PaymentMethod,
    FinalRegister,
    Department,
    DoctorName,
    PatientName,
    PrescriptionThrough,
    City,
    Market,
    Revenue,
    MedicineBarcode,
    EntranceImage,
    MedicineWith,
    RevenueRecord,
    BigCompany,
    MedicineConflict,
    PurchaseListManual,
    GlobalSettings
)

from django_jalali.admin.filters import JDateFieldListFilter
from django.contrib.auth.admin import UserAdmin
from .models import User, AdditionalPermission


UserAdmin.list_display += ("image",)
UserAdmin.list_filter += ("image",)

UserAdmin.list_display += ("get_additional_permissions",)
UserAdmin.fieldsets += (
    ("Extra Fields", {"fields": ("image", "additional_permissions")}),
)

class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('barcode_type',)
    fieldsets = (
        (None, {
            'fields': ('barcode_type',),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            return qs.filter(pk=GlobalSettings.get_settings().pk)
        except GlobalSettings.DoesNotExist:
            return qs.none()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(GlobalSettings, GlobalSettingsAdmin)


class ImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    skip_admin_log = True
    IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = False
    pass


class EntracnceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = (("factor_date", JDateFieldListFilter),)


class MedicineImport(resources.ModelResource):
    kind = fields.Field(
        column_name="kind",
        attribute="name_persian",
        widget=ForeignKeyWidget(Kind, "name_persian"),
    )
    big_company = fields.Field(
        column_name="big_company",
        attribute="big_company",
        widget=ForeignKeyWidget(BigCompany, "name"),
    )
    pharm_group = fields.Field(
        column_name="pharm_group",
        attribute="pharm_group",
        widget=ForeignKeyWidget(PharmGroup, "name_english"),
    )
    country = fields.Field(
        column_name="country",
        attribute="country",
        widget=ForeignKeyWidget(Country, "name"),
    )

    class Meta:
        model = Medician



class EntranceThrougheAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = (
        "register_quantity",
        "each_purchase_price",
        "total_sell",
        "bonus_interest",
        "total_purchaseـafghani",
        "total_purchaseـcurrency",
        "total_interest",
        "each_price",
        "total_purchase_currency_before",
        "discount_value",
        "each_quantity",
        "bonus_value",
        "each_sell_price",
        "interest_money",
    )


class PrescriptionThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ("total_price",)


class MedicineAdmin(ImportExportModelAdmin):
    resource_class = MedicineImport


admin.site.register(User, UserAdmin)
admin.site.register(AdditionalPermission, ImportAdmin)
admin.site.register(PharmGroup, ImportAdmin)
admin.site.register(Medician, MedicineAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(RevenueRecord, ImportAdmin)
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
admin.site.register(BigCompany, ImportAdmin)
admin.site.register(DoctorName, ImportAdmin)
admin.site.register(City, ImportAdmin)
admin.site.register(Market, ImportAdmin)
admin.site.register(PatientName, ImportAdmin)
admin.site.register(Revenue, ImportAdmin)
admin.site.register(MedicineConflict, ImportAdmin)
admin.site.register(PrescriptionThrough, PrescriptionThroughAdmin)

# Register your models here.
