from django.urls import path, include
from rest_framework import routers

from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView, UnitView, PharmCompanyView, \
    StoreView, FinalRegisterView, PrescriptionThroughView, PatientNameView, DoctorNameView, DepartmentView, CurrencyView, \
    PaymentMethodView, EntranceThroughView, EntranceView, OutranceView, OutranceThroughView, MedicianExcelView, TrazView



router = routers.DefaultRouter()
router.register(r'medician', MedicianView)
router.register(r'kind', KindView)
router.register(r'pharm-groub', PharmGroupView)
router.register(r'country', CountryView)
router.register(r'prescription', PrescriptionView)
router.register(r'unit', UnitView)
router.register(r'pharm-companies', PharmCompanyView)
router.register(r'entrance', EntranceView)
router.register(r'entrance-throug', EntranceThroughView)
router.register(r'store', StoreView)
router.register(r'final-register', FinalRegisterView)
router.register(r'prescription-through', PrescriptionThroughView)
router.register(r'patient', PatientNameView)
router.register(r'doctor', DoctorNameView)
router.register(r'department', DepartmentView)
router.register(r'currency', CurrencyView)
router.register(r'payment-method', PaymentMethodView)
router.register(r'outrance', OutranceView)
router.register(r'outrance-through', OutranceThroughView)
router.register(r'medician-excel', MedicianExcelView)
router.register(r'traz', TrazView, basename='traz')





urlpatterns = [
    path('', include(router.urls)),
]
