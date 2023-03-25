from django.urls import path, include
from rest_framework import routers

from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView, UnitView, PharmCompanyView, EntranceView

router = routers.DefaultRouter()
router.register(r'medician', MedicianView)
router.register(r'kind', KindView)
router.register(r'pharm-groub', PharmGroupView)
router.register(r'country', CountryView)
router.register(r'prescription', PrescriptionView)
router.register(r'unit', UnitView)
router.register(r'pharm-companies', PharmCompanyView)
router.register(r'entrances', EntranceView)


urlpatterns = [
    path('', include(router.urls)),
]
