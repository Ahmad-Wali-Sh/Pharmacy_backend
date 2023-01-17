from django.urls import path , include
from rest_framework import routers

from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView, UnitView

router = routers.DefaultRouter()
router.register(r'medician', MedicianView)
router.register(r'kind', KindView)
router.register(r'pharm-groub', PharmGroupView)
router.register(r'country', CountryView)
router.register(r'prescription', PrescriptionView)
router.register(r'unit', UnitView)


urlpatterns = [ 
    path('', include(router.urls)),
]