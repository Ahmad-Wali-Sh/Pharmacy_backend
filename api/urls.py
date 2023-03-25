from django.urls import path, include
from rest_framework import routers

<<<<<<< HEAD
from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView, UnitView, PharmCompanyView, EntranceView
=======
from .views import MedicianView, PharmGroupView, CountryView, KindView, PrescriptionView, UnitView, PharmCompanyView, \
                   EntranceView, EntranceThroughView
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2

router = routers.DefaultRouter()
router.register(r'medician', MedicianView)
router.register(r'kind', KindView)
router.register(r'pharm-groub', PharmGroupView)
router.register(r'country', CountryView)
router.register(r'prescription', PrescriptionView)
router.register(r'unit', UnitView)
router.register(r'pharm-companies', PharmCompanyView)
<<<<<<< HEAD
router.register(r'entrances', EntranceView)
=======
router.register(r'entrance', EntranceView)
router.register(r'entrance-throug', EntranceThroughView)
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2


urlpatterns = [
    path('', include(router.urls)),
]
