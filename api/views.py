from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer, \
    StoreSerializer, CurrencySerializer, EntranceSerializer, EntranceThroughSerializer, PaymentMethodSerializer, FinalRegisterSerializer, DepartmentSerializer, \
    DoctorNameSerializer, PatientNameSerializer, PrescriptionThroughSerializer, OutranceSerializer, OutranceThroughSerializer, MeidicainExcelSerializer, TrazSerializer, \
    CitySerializer, MarketSerializer, RevenueSerializer, RevenueTrhoughSerializer, UserSerializer
    
from rest_framework.pagination import PageNumberPagination
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, Outrance, OutranceThrough, \
    City, Market, Revenue, RevenueTrough, User
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .permissions import D7896DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_multiple_model.viewsets import FlatMultipleModelAPIViewSet


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50



class MedicianFilter(django_filters.FilterSet):
    generic_name = django_filters.CharFilter(lookup_expr="icontains")
    barcode = django_filters.CharFilter(lookup_expr="icontains")
    brand_name = django_filters.CharFilter(lookup_expr="icontains")
    ml = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Medician
        fields = ['brand_name', 'generic_name', 'no_pocket', "ml", "location", "barcode", "company","price","existence","pharm_group","kind", "country",]

class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianSeralizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name', 'barcode', 'generic_name', 'ml']
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    
class MedicianExcelView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MeidicainExcelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name']
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]

class UserView (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [D7896DjangoModelPermissions]
    


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'phone', 'address']
    search_fields = ['name',]



class FinalRegisterView(viewsets.ModelViewSet):
    queryset = FinalRegister.objects.all()
    serializer_class = FinalRegisterSerializer
    permission_classes = [D7896DjangoModelPermissions]

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [D7896DjangoModelPermissions]

class RevenueFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter() 

    class Meta:
        model = Revenue
        fields = ['created', 'active','employee', 'revenue_through__prescription_number']


class RevenueView(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = RevenueFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]

class RevenueThroughView(viewsets.ModelViewSet):
    queryset = RevenueTrough.objects.all()
    serializer_class = RevenueTrhoughSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['revenue',]

class MarketView(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [D7896DjangoModelPermissions]

class PrescriptionThroughView(viewsets.ModelViewSet):
    queryset = PrescriptionThrough.objects.all()
    serializer_class = PrescriptionThroughSerializer
    filterset_fields = ['prescription',]
    permission_classes = [D7896DjangoModelPermissions]


class PatientNameView(viewsets.ModelViewSet):
    queryset = PatientName.objects.all()
    serializer_class = PatientNameSerializer
    permission_classes = [D7896DjangoModelPermissions]


class DoctorNameView(viewsets.ModelViewSet):
    queryset = DoctorName.objects.all()
    serializer_class = DoctorNameSerializer
    permission_classes = [D7896DjangoModelPermissions]


class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [D7896DjangoModelPermissions]


class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [D7896DjangoModelPermissions]


class PaymentMethodView(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [D7896DjangoModelPermissions]


class KindView(viewsets.ModelViewSet):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['name_english', 'name_persian']
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ['name',]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]


class PharmGroupView(viewsets.ModelViewSet):
    queryset = PharmGroup.objects.all()
    serializer_class = PharmGroupSeralizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['name_english', 'name_persian']
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]

class PrescriptionFilterView(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter() 
    class Meta:
        model = Prescription
        fields =['prescription_number','department', 'created', 'name', 'doctor', 'prescription_number', 'sold']

class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filterset_class = PrescriptionFilterView
    permission_classes = [D7896DjangoModelPermissions]


class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSeralizer
    permission_classes = [D7896DjangoModelPermissions]


class PharmCompanyView(viewsets.ModelViewSet):
    queryset = PharmCompany.objects.all()
    serializer_class = PharmCompanySeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    permission_classes = [D7896DjangoModelPermissions]

class EntranceFilterView(django_filters.FilterSet):
    factor_date = django_filters.DateFromToRangeFilter() 
    class Meta:
        model = Entrance
        fields = ['factor_number', 'factor_date', 'total_interest', 'company', 'payment_method','final_register', 'store']


class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all()
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceFilterView

class EntranceThroughView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all()
    serializer_class = EntranceThroughSerializer
    filterset_fields = ('entrance','medician')
    permission_classes = [D7896DjangoModelPermissions]


class OutranceView (viewsets.ModelViewSet):
    queryset = Outrance.objects.all()
    serializer_class = OutranceSerializer
    permission_classes = [D7896DjangoModelPermissions]

class OutranceThroughView (viewsets.ModelViewSet):
    queryset = OutranceThrough.objects.all()
    serializer_class = OutranceThroughSerializer
    filterset_fields = ('outrance',)
    permission_classes = [D7896DjangoModelPermissions]

from rest_framework import permissions

class MultipleModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        return True



class TrazView (FlatMultipleModelAPIViewSet):
        
    querylist = [
        {'queryset': EntranceThrough.objects.all(), 'serializer_class': EntranceThroughSerializer},
        {'queryset': PrescriptionThrough.objects.all(), 'serializer_class': PrescriptionThroughSerializer},
        {'queryset': OutranceThrough.objects.all(), 'serializer_class': OutranceThroughSerializer},
    ]
    model = EntranceThrough
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ('medician',)
    ordering_fields = ['id','timestamp']
    ordering = ['id','timestamp']
    




