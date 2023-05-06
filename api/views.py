from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer, \
    StoreSerializer, CurrencySerializer, EntranceSerializer, EntranceThroughSerializer, PaymentMethodSerializer, FinalRegisterSerializer, DepartmentSerializer, \
    DoctorNameSerializer, PatientNameSerializer, PrescriptionThroughSerializer
from rest_framework.pagination import PageNumberPagination
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianSeralizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('brand_name',)
    search_fields = ['brand_name']


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class FinalRegisterView(viewsets.ModelViewSet):
    queryset = FinalRegister.objects.all()
    serializer_class = FinalRegisterSerializer


class PrescriptionThroughView(viewsets.ModelViewSet):
    queryset = PrescriptionThrough.objects.all()
    serializer_class = PrescriptionThroughSerializer
    filterset_fields = ['prescription',]


class PatientNameView(viewsets.ModelViewSet):
    queryset = PatientName.objects.all()
    serializer_class = PatientNameSerializer


class DoctorNameView(viewsets.ModelViewSet):
    queryset = DoctorName.objects.all()
    serializer_class = DoctorNameSerializer


class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class PaymentMethodView(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


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


class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all()
    serializer_class = EntranceSerializer


class EntranceThroughView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all()
    serializer_class = EntranceThroughSerializer
    filterset_fields = ('entrance',)
