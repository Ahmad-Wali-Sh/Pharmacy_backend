from django.urls import path, include
from rest_framework import routers

from .views import (
    MedicianView,
    PharmGroupView,
    CountryView,
    KindView,
    PrescriptionView,
    UnitView,
    PharmCompanyView,
    StoreView,
    FinalRegisterView,
    PrescriptionThroughView,
    PatientNameView,
    DoctorNameView,
    DepartmentView,
    CurrencyView,
    PaymentMethodView,
    EntranceThroughView,
    EntranceView,
    PrescriptionReturnThroughView,
    PrescriptionReturnView,
    PrescriptionReturnPaginatedView,
    LastPrescriptionReturnView,
    PrescriptionReturnImageView,
    DepartmentReturnView,
    EntrancePaginatedView,
    MedicianExcelView,
    TrazView,
    CityView,
    MarketView,
    RevenueView,
    LastEntranceView,
    MedicineWithView,
    LastPrescriptionView,
    BigCompanyView,
    EntranceThroughExpiresView,
    user_permissions,
    StockView,
    StockExcelView,
    MedicianOrderViewSet,
    MedicineConflictView,
    MedicineBarcodeView,
    PrescriptionReturnViewSet,
    PuchaseListView,
    MedicianMinimumViewSet,
    PrescriptionImageView,
    EntranceImageView,
    PrescriptionExcelView,
    PurchaseListQueryView,
    PurchaseListManualView,
    PrescriptionPaginatedView,
    RevenueRecordViewSet,
    PrescriptionViewSet,
    JournalEntryView,
    JournalCategoryView
)

prescription_extra_actions = {
    "previous": "previous",
}


router = routers.DefaultRouter()
router.register(r"medician", MedicianView)
router.register(r"kind", KindView)
router.register(r"pharm-groub", PharmGroupView)
router.register(r"country", CountryView)
router.register(r"prescription", PrescriptionView)
router.register(r"prescription-return", PrescriptionReturnView)
router.register(r"unit", UnitView)
router.register(r"medicine-barcode", MedicineBarcodeView)
router.register(r"pharm-companies", PharmCompanyView)
router.register(r"entrance", EntranceView)
router.register(r"entrance-pg", EntrancePaginatedView, basename='entrance-paginated')
router.register(r"entrance-image", EntranceImageView)
router.register(r"prescription-image", PrescriptionImageView)
router.register(r"prescription-return-image", PrescriptionReturnImageView)
router.register(r"entrance-throug", EntranceThroughView)
router.register(r"store", StoreView)
router.register(r"final-register", FinalRegisterView)
router.register(r"prescription-through", PrescriptionThroughView)
router.register(r"prescription-return-through", PrescriptionReturnThroughView)
router.register(r"patient", PatientNameView)
router.register(r"doctor", DoctorNameView)
router.register(r"department", DepartmentView)
router.register(r"department-return", DepartmentReturnView)
router.register(r"currency", CurrencyView)
router.register(r"payment-method", PaymentMethodView)
router.register(r"revenue", RevenueView)
router.register(r"medician-excel", MedicianExcelView, basename='medicine-excel')
router.register(r"prescription-pg", PrescriptionPaginatedView, basename='prescription-pg')
router.register(r"prescription-return-pg", PrescriptionReturnPaginatedView, basename='prescription-return-pg')
router.register(r"last-entrance", LastEntranceView, basename='last-entrance')
router.register(r"last-prescription-return", LastPrescriptionReturnView, basename='last-prescription-return')
router.register(r"last-prescription", LastPrescriptionView, basename='last-prescription')
router.register(r"big-company", BigCompanyView)
router.register(r"purchase-list", PurchaseListQueryView, basename='purchase-list')
router.register(r"city", CityView)
router.register(r"medicine-with", MedicineWithView)
router.register(r"revenue-record", RevenueRecordViewSet)
router.register(r"purchase-list-manual", PurchaseListManualView, basename='purchase-list-manual')
router.register(r"medicine_order", MedicianOrderViewSet, basename='medicine-order')
router.register(r"medicine_minimum", MedicianMinimumViewSet, basename='medicine-minimum')
router.register(r"medicine-conflict", MedicineConflictView, basename='medicien-conflict')
router.register(r"journal-category", JournalCategoryView, basename='journal-category')
router.register(r"journal-entry", JournalEntryView, basename='journal-entry')
router.register(r"stock", StockView, basename='stock')
router.register(r"stock-excel", StockExcelView, basename='stock-excel')
router.register(r"prescription-excel", PrescriptionExcelView, basename='prescription-excel')
router.register(
    r"entrance-through-expired", EntranceThroughExpiresView, basename="medicines"
)
router.register(r"market", MarketView)
router.register(r"traz", TrazView, basename="traz")


urlpatterns = [
    path("", include(router.urls)),
    path("user/permissions/", user_permissions, name="user_permissions"),
    path(
        "prescription/<int:pk>/previous/",
        PrescriptionViewSet.as_view({"get": "previous"}),
        name="prescription-previous",
    ),
    path(
        "prescription/<int:pk>/next/",
        PrescriptionViewSet.as_view({"get": "next"}),
        name="prescription-next",
    ),
    path(
        "prescription-return/<int:pk>/previous/",
        PrescriptionReturnViewSet.as_view({"get": "previous"}),
        name="prescription-previous",
    ),
    path(
        "prescription-return/<int:pk>/next/",
        PrescriptionReturnViewSet.as_view({"get": "next"}),
        name="prescription-next",
    ),
]
