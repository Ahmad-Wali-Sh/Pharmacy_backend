from rest_framework import viewsets

<<<<<<< HEAD
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, Entrance

from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer, EntranceSeralizer
=======
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, EntranceThrough, Entrance

from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer , \
                         EntranceThroughSerializer, EntranceSerializer 
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianSeralizer


class KindView(viewsets.ModelViewSet):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class PharmGroupView(viewsets.ModelViewSet):
    queryset = PharmGroup.objects.all()
    serializer_class = PharmGroupSeralizer


class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSeralizer


class PharmCompanyView(viewsets.ModelViewSet):
    queryset = PharmCompany.objects.all()
    serializer_class = PharmCompanySeralizer

<<<<<<< HEAD

class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all()
    serializer_class = EntranceSeralizer
=======
class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all()
    serializer_class = EntranceSerializer

class EntranceThroughView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all()
    serializer_class = EntranceThroughSerializer
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2
