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
    OutranceView,
    OutranceThroughView,
    MedicianExcelView,
    TrazView,
    CityView,
    MarketView,
    RevenueThroughView,
    RevenueView,
    LastEntranceView,
    MedicineWithView,
    LastPrescriptionView,
    BigCompanyView,
    EntranceThroughExpiresView,
    user_permissions,
    MedicineConflictView,
    MedicineBarcodeView,
    PuchaseListView,
    PrescriptionImageView,
    EntranceImageView,
    PurchaseListQueryView,
    PurchaseListManualView,
    PrescriptionPaginatedView,
    PrescriptionViewSet
)

prescription_extra_actions = {
    'previous': 'previous',
}



router = routers.DefaultRouter()
router.register(r"medician", MedicianView)
router.register(r"kind", KindView)
router.register(r"pharm-groub", PharmGroupView)
router.register(r"country", CountryView)
router.register(r"prescription", PrescriptionView)
router.register(r"unit", UnitView)
router.register(r"medicine-barcode", MedicineBarcodeView)
router.register(r"pharm-companies", PharmCompanyView)
router.register(r"entrance", EntranceView)
router.register(r"entrance-image", EntranceImageView)
router.register(r"prescription-image", PrescriptionImageView)
router.register(r"entrance-throug", EntranceThroughView)
router.register(r"store", StoreView)
router.register(r"final-register", FinalRegisterView)
router.register(r"prescription-through", PrescriptionThroughView)
router.register(r"patient", PatientNameView)
router.register(r"doctor", DoctorNameView)
router.register(r"department", DepartmentView)
router.register(r"currency", CurrencyView)
router.register(r"payment-method", PaymentMethodView)
router.register(r"outrance", OutranceView)
router.register(r"revenue", RevenueView)
router.register(r"revenue-through", RevenueThroughView)
router.register(r"outrance-through", OutranceThroughView)
router.register(r"medician-excel", MedicianExcelView)
router.register(r"prescription-pg", PrescriptionPaginatedView)
router.register(r"last-entrance", LastEntranceView)
router.register(r"last-prescription", LastPrescriptionView)
router.register(r"big-company", BigCompanyView)
router.register(r"purchase-list", PurchaseListQueryView)
router.register(r"city", CityView)
router.register(r"medicine-with", MedicineWithView)
router.register(r"purchase-list-manual", PurchaseListManualView)
router.register(r"medicine-conflict", MedicineConflictView)
router.register(
    r"entrance-through-expired", EntranceThroughExpiresView, basename="medicines"
)
router.register(r"market", MarketView)
router.register(r"traz", TrazView, basename="traz")


urlpatterns = [
    path("", include(router.urls)),
    path("user/permissions/", user_permissions, name="user_permissions"),
    path('prescription/<int:pk>/previous/', PrescriptionViewSet.as_view({'get': 'previous'}), name='prescription-previous'),
    path('prescription/<int:pk>/next/', PrescriptionViewSet.as_view({'get': 'next'}), name='prescription-next'),
]
