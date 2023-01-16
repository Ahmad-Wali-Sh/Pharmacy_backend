from django.urls import path , include
from rest_framework import routers

from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView

router = routers.DefaultRouter()
router.register(r'medician', MedicianView)
router.register(r'kind', KindView)
router.register(r'pharm-groub', PharmGroupView)
router.register(r'country', CountryView)
router.register(r'prescription', PrescriptionView)


urlpatterns = [ 
    path('', include(router.urls)),
]