from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from excel_response import ExcelResponse
from datetime import datetime


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
    PrescriptionReturn,
    PrescriptionReturnThrough,
    PrescriptionReturnImage,
    DepartmentReturn,
    MedicineSaleDictionary,
    PrescriptionThrough,
    City,
    Market,
    Revenue,
    MedicineBarcode,
    EntranceImage,
    MedicineWith,
    RevenueRecord,
    JournalCategory, 
    JournalEntry,
    BigCompany,
    MedicineConflict,
    PurchaseListManual,
    GlobalSettings,
    SalaryEntry
)

from django_jalali.admin.filters import JDateFieldListFilter
from .models import AdditionalPermission


class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'barcode_type',
        'ticket_paper_width',
        'detailed_paper_width',
        'ticket_printer',
        'detailed_printer' 
    )
    fieldsets = (
        ('Barcode Settings', {
            'fields': (
                'barcode_type',
            )
        }),
        ('Ticket Print Settings', {
            'fields': (
                'ticket_paper_width', 
                'ticket_fields',
                'ticket_printer',
            )
        }),
        ('Detailed Print Settings', {
            'fields': (
                'detailed_paper_width',
                'detailed_fields',
                'detailed_printer',
                'detailed_text_font'
            )
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

class AdditionalPermissionsAdmin (admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
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
    list_display = (
        'id',
        'medician',
        'entrance',
        'register_quantity',
        'each_quantity',
    )


class PrescriptionThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ("total_price",)
    list_display = (
        'id',
        'medician',
        'prescription',
        'quantity',
    )


class MedicineAdmin(ImportExportModelAdmin):
    resource_class = MedicineImport
    list_display = (
        'id',
        'get_medicine_full',
        'price',
        'existence',
    )
    search_fields = ('brand_name', 'generic_name__contains', 'barcode__contains')
    list_filter = ('kind', 'pharm_group', 'country', 'big_company', 'active')
    ordering = ('brand_name',)
    actions = ['export_to_excel']

    def get_medicine_full(self, obj):
        kind_name = f"{obj.kind.name_english}." if obj.kind else ""
        country_name = f"{obj.country.name}" if obj.country else ""
        big_company_name = f"{obj.big_company.name} " if obj.big_company else ""
        generics = (
            f"{{{','.join(map(str, obj.generic_name))}}}"
            if obj.generic_name
            else ""
        )
        ml = f"{obj.ml}" if obj.ml else ""
        weight = f"{obj.weight}" if obj.weight else ""

        medicine_full = (
            f"{kind_name}{obj.brand_name} {ml} {big_company_name}{country_name} {weight}"
        )
        return medicine_full

    get_medicine_full.short_description = 'Medicine Full'

    def export_to_excel(self, request, queryset):
        data = [
            ['آی دی', 'دارو', 'قیمت', 'موجودی'],
        ]
        
        today_date = datetime.now().strftime("%Y-%m-%d")
        excel_export_name = f'Medicine_List_{today_date}'
        for obj in queryset:
            medicine_full = obj.get_medicine_full(obj)
            data.append([obj.id, medicine_full, obj.price, obj.existence])
        
        response = ExcelResponse(data, excel_export_name)
        return response

    export_to_excel.short_description = 'Export to Excel'



admin.site.register(AdditionalPermission, AdditionalPermissionsAdmin)
admin.site.register(PharmGroup, ImportAdmin)
admin.site.register(Medician, MedicineAdmin)
admin.site.register(Kind, ImportAdmin)
admin.site.register(Country, ImportAdmin)
admin.site.register(PrescriptionReturn, ImportAdmin)
admin.site.register(PrescriptionReturnThrough, ImportAdmin)
admin.site.register(PrescriptionReturnImage, ImportAdmin)
admin.site.register(DepartmentReturn, ImportAdmin)
admin.site.register(Unit, ImportAdmin)
admin.site.register(RevenueRecord, ImportAdmin)
admin.site.register(Prescription, ImportAdmin)
admin.site.register(MedicineSaleDictionary, ImportAdmin)
admin.site.register(PharmCompany, ImportAdmin)
admin.site.register(Entrance, EntracnceAdmin)
admin.site.register(MedicineBarcode, ImportAdmin)
admin.site.register(Store, ImportAdmin)
admin.site.register(PurchaseListManual, ImportAdmin)
admin.site.register(JournalEntry, ImportAdmin)
admin.site.register(JournalCategory, ImportAdmin)
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
admin.site.register(SalaryEntry, ImportAdmin)
admin.site.register(PatientName, ImportAdmin)
admin.site.register(Revenue, ImportAdmin)
admin.site.register(MedicineConflict, ImportAdmin)
admin.site.register(PrescriptionThrough, PrescriptionThroughAdmin)

# Register your models here.
