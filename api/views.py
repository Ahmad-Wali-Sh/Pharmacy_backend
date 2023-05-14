from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer, \
    StoreSerializer, CurrencySerializer, EntranceSerializer, EntranceThroughSerializer, PaymentMethodSerializer, FinalRegisterSerializer, DepartmentSerializer, \
    DoctorNameSerializer, PatientNameSerializer, PrescriptionThroughSerializer, OutranceSerializer, OutranceThroughSerializer, MeidicainExcelSerializer
from rest_framework.pagination import PageNumberPagination
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, Outrance, OutranceThrough
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class MedicianFilter(django_filters.FilterSet):
    generic_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Medician
        fields = ('brand_name', 'generic_name', 'no_pocket', "ml", "location", "barcode", "company","price","existence","pharm_group","kind", "country",)

class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianSeralizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name']
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    
class MedicianExcelView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MeidicainExcelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name']
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    


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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['name_english', 'name_persian']
    ordering_fields = ['id',]
    ordering = ['id',]


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ['name',]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['id',]


class PharmGroupView(viewsets.ModelViewSet):
    queryset = PharmGroup.objects.all()
    serializer_class = PharmGroupSeralizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['name_english', 'name_persian']
    ordering_fields = ['id',]
    ordering = ['id',]


class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filterset_fields = ['prescription_number',]


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

class OutranceView (viewsets.ModelViewSet):
    queryset = Outrance.objects.all()
    serializer_class = OutranceSerializer

class OutranceThroughView (viewsets.ModelViewSet):
    queryset = OutranceThrough.objects.all()
    serializer_class = OutranceThroughSerializer
    filterset_fields = ('outrance',)