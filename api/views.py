from rest_framework import permissions
from .serializers import PharmGroupSeralizer, MedicianSeralizer, PharmCompanySeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer, \
    StoreSerializer, CurrencySerializer, EntranceSerializer, EntranceThroughSerializer, PaymentMethodSerializer, FinalRegisterSerializer, DepartmentSerializer, \
    DoctorNameSerializer, PatientNameSerializer, PrescriptionThroughSerializer, OutranceSerializer, OutranceThroughSerializer, MeidicainExcelSerializer, TrazSerializer, \
    CitySerializer, MarketSerializer, RevenueSerializer, RevenueTrhoughSerializer, UserSerializer, MedicineWithSerializer, BigCompanySerializer, EntranceThroughExpiresSerializer, MedicineConflictSerializer, \
    PurchaseListSerializer, PurchaseListQuerySerializer, PurchaseListManualSerializer, EntranceImageSeriazlier

from rest_framework.pagination import PageNumberPagination
from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, Outrance, OutranceThrough, \
    City, Market, Revenue, RevenueTrough, User, EntranceImage, MedicineWith, BigCompany, MedicineConflict, PurchaseList, PurchaseListManual
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .permissions import D7896DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from dateutil.relativedelta import relativedelta
from datetime import date

from drf_multiple_model.viewsets import FlatMultipleModelAPIViewSet
from django.contrib.postgres.forms.array import SimpleArrayField
from django_filters.filters import Filter
from django.db import models
from django.db.models import F
from django_filters.fields import Lookup
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.request import Request


class ArrayOverlapFilter(Filter):
    field_class = SimpleArrayField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "overlap")
        super().__init__(*args, **kwargs)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


def filter_by_ids(queryset, name, value):
    values = value.split(',')
    return queryset.filter(id__in=values)


def filter_by_generics(queryset, name, value):
    values = value.split(',')
    return queryset.filter(generic_name=values)


class CharArrayFilter(django_filters.BaseCSVFilter, django_filters.CharFilter):
    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ListFilter(Filter):
    def filter(self, qs, value):
        value_list = value.split(u',')
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class MedicianFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method=filter_by_ids)
    generic_name = django_filters.BaseInFilter(
        lookup_expr='contains', method=filter_by_generics)
    brand_name = django_filters.CharFilter(lookup_expr="istartswith")
    all = django_filters.CharFilter(method='all_filter', label='allSearch')
    ml = django_filters.CharFilter(lookup_expr='icontains')
    kind__name_english = django_filters.CharFilter(lookup_expr='icontains')
    kind__name_persian = django_filters.CharFilter(lookup_expr='icontains')
    country__name = django_filters.CharFilter(lookup_expr='icontains')
    big_company__name = django_filters.CharFilter(lookup_expr='icontains')
    barcode__contains = CharArrayFilter(
        lookup_expr='contains', field_name='barcode')

    def all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(brand_name__icontains=value) |
            Q(generic_name__icontains=value) |
            Q(ml__icontains=value) |
            Q(country__name__icontains=value) |
            Q(kind__name_english=value) |
            Q(kind__name_persian=value) |
            Q(big_company__name=value)
        )

    class Meta:
        model = Medician
        filter_fields = {
            'barcode': ['exact', 'icontains']
        }
        fields = ['brand_name', 'all', 'generic_name', 'no_pocket', "ml", "location", "barcode__contains", "company", "price", "existence",
                  "pharm_group", "kind", "country", 'department', 'id', 'ids', "kind__name_english", "country__name", 'kind__name_persian', 'big_company__name']


class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all().order_by('id')
    serializer_class = MedicianSeralizer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["generic_name"]
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination


class MedicianExcelView(viewsets.ModelViewSet):
    queryset = Medician.objects.all().order_by('id')
    serializer_class = MeidicainExcelSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name']
    filterset_class = MedicianFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]


class UserView (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [D7896DjangoModelPermissions]

class StoreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by('id')
    serializer_class = StoreSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = StoreFilter
    search_fields = ['name',]


class FinalRegisterView(viewsets.ModelViewSet):
    queryset = FinalRegister.objects.all().order_by('id')
    serializer_class = FinalRegisterSerializer
    permission_classes = [D7896DjangoModelPermissions]


class PuchaseListView(viewsets.ModelViewSet):
    queryset = PurchaseList.objects.all().order_by('id')
    serializer_class = PurchaseListSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'company_1__market', 'company_1']
    ordering = ['id',]
    
class CityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CityFilter
    permission_classes = [D7896DjangoModelPermissions]


class RevenueFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Revenue
        fields = ['created', 'active', 'employee',
                  'revenue_through__prescription_number']


class RevenueView(viewsets.ModelViewSet):
    queryset = Revenue.objects.all().order_by('id')
    serializer_class = RevenueSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RevenueFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]


class RevenueThroughView(viewsets.ModelViewSet):
    queryset = RevenueTrough.objects.all().order_by('id')
    serializer_class = RevenueTrhoughSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['revenue',]


class MarketFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

class MarketView(viewsets.ModelViewSet):
    queryset = Market.objects.all().order_by('id')
    serializer_class = MarketSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MarketFilter


class PrescriptionThroughView(viewsets.ModelViewSet):
    queryset = PrescriptionThrough.objects.all().order_by("id")
    serializer_class = PrescriptionThroughSerializer
    filterset_fields = ['prescription',]
    permission_classes = [D7896DjangoModelPermissions]

    @action(methods=['DELETE', 'GET'], detail=False,)
    def delete(self, request: Request):
        delete_id = request.GET['prescription']
        print(request.GET['prescription'])
        delete_prescriptions = self.queryset.filter(prescription=delete_id)
        delete_prescriptions.delete()
        return Response(self.serializer_class(delete_prescriptions, many=True).data)


class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = PatientName
        fields = ['name', 'contact_number', 'id', 'gender', "tazkira_number"]


class PatientNameView(viewsets.ModelViewSet):
    queryset = PatientName.objects.all().order_by('id')
    serializer_class = PatientNameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PatientFilter
    permission_classes = [D7896DjangoModelPermissions]


class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DoctorName
        fields = ['name', 'contact_number', 'id', 'expertise']


class DoctorNameView(viewsets.ModelViewSet):
    queryset = DoctorName.objects.all().order_by('id')
    serializer_class = DoctorNameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorFilter
    permission_classes = [D7896DjangoModelPermissions]

class BigCompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = BigCompany
        fields = ['name',]

class BigCompanyView(viewsets.ModelViewSet):
    queryset = BigCompany.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = BigCompanySerializer
    filterset_class = BigCompanyFilter
    permission_classes = [D7896DjangoModelPermissions]


class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name',]
    ordering_fields = ['id',]


class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('id')
    serializer_class = CurrencySerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['id',]


class PaymentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')


class PaymentMethodView(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all().order_by('id')
    serializer_class = PaymentMethodSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PaymentFilter


class KindFilter(django_filters.FilterSet):
    name_english = django_filters.CharFilter(lookup_expr='icontains')
    name_persian = django_filters.CharFilter(lookup_expr='icontains')


class KindView(viewsets.ModelViewSet):
    queryset = Kind.objects.all().order_by('id')
    serializer_class = KindSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = KindFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]

class CountryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('id')
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]

class PharmGroupFilter(django_filters.FilterSet):
    name_english = django_filters.CharFilter(lookup_expr='icontains')
    name_persian = django_filters.CharFilter(lookup_expr='icontains')


class PharmGroupView(viewsets.ModelViewSet):
    queryset = PharmGroup.objects.all().order_by('id')
    serializer_class = PharmGroupSeralizer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PharmGroupFilter
    ordering_fields = ['id',]
    ordering = ['id',]
    permission_classes = [D7896DjangoModelPermissions]


class PrescriptionFilterView(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Prescription
        fields = ['prescription_number', 'department', 'created',
                  'name', 'doctor', 'prescription_number', 'sold', 'barcode_str']


class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by('id')
    serializer_class = PrescriptionSerializer
    filterset_class = PrescriptionFilterView
    permission_classes = [D7896DjangoModelPermissions]


class LastPrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by('-id')[:1]
    serializer_class = PrescriptionSerializer
    permission_classes = [D7896DjangoModelPermissions]


class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSeralizer
    permission_classes = [D7896DjangoModelPermissions]


class PharmCompanyView(viewsets.ModelViewSet):
    queryset = PharmCompany.objects.all().order_by('id')
    serializer_class = PharmCompanySeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    permission_classes = [D7896DjangoModelPermissions]


class EntranceFilterView(django_filters.FilterSet):
    factor_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Entrance
        fields = ['factor_number', 'factor_date', 'total_interest',
                  'company', 'payment_method', 'final_register', 'store']


class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by('id')
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceFilterView

class EntranceImageView(viewsets.ModelViewSet):
    queryset = EntranceImage.objects.all().order_by('id')
    serializer_class = EntranceImageSeriazlier
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['entrance',]


class LastEntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by('-id')[:1]
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]


class EntranceThroughFilterView(django_filters.FilterSet):

    class Meta:
        model = EntranceThrough
        fields = ['entrance', 'medician', 'medician__ml']


class EntranceThroughView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all().order_by('id')
    serializer_class = EntranceThroughSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['medician__generic_name',]
    filterset_class = EntranceThroughFilterView
    permission_classes = [D7896DjangoModelPermissions]


class EntranceThroughExpiresView(viewsets.ModelViewSet):
    serializer_class = EntranceThroughExpiresSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['medician__generic_name',]
    filterset_class = EntranceThroughFilterView
    permission_classes = [D7896DjangoModelPermissions]

    def get_queryset(self):
        medicines = EntranceThrough.objects.filter(
            expire_date__lte=date.today() + relativedelta(months=6))
        return medicines


class OutranceView (viewsets.ModelViewSet):
    queryset = Outrance.objects.all().order_by('id')
    serializer_class = OutranceSerializer
    permission_classes = [D7896DjangoModelPermissions]


class MedicineWithView (viewsets.ModelViewSet):
    queryset = MedicineWith.objects.all().order_by('id')
    serializer_class = MedicineWithSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filterset_fields = ('medicine',)


class PurchaseListQueryView (viewsets.ModelViewSet):
    queryset = Medician.objects.filter(to_buy=True).filter(shorted=False) | Medician.objects.filter(
        existence__lt=F('minmum_existence')).filter(shorted=False)
    serializer_class = PurchaseListQuerySerializer
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id',]
    ordering = ['id',]


class MedicineConflictView (viewsets.ModelViewSet):
    queryset = MedicineConflict.objects.all().order_by('id')
    serializer_class = MedicineConflictSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filterset_fields = ('medicine_1',)


class OutranceThroughView (viewsets.ModelViewSet):
    queryset = OutranceThrough.objects.all().order_by('id')
    serializer_class = OutranceThroughSerializer
    filterset_fields = ('outrance',)
    permission_classes = [D7896DjangoModelPermissions]


class MultipleModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        return True


class TrazView (FlatMultipleModelAPIViewSet):

    querylist = [
        {'queryset': EntranceThrough.objects.all(
        ), 'serializer_class': EntranceThroughSerializer},
        {'queryset': PrescriptionThrough.objects.all(
        ), 'serializer_class': PrescriptionThroughSerializer},
        {'queryset': OutranceThrough.objects.all(
        ), 'serializer_class': OutranceThroughSerializer},
    ]
    model = EntranceThrough
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('medician',)
    ordering_fields = ['id', 'timestamp']
    ordering = ['id', 'timestamp']


class PurchaseListManualView (viewsets.ModelViewSet):
    queryset = PurchaseListManual.objects.all().order_by('-id')
    serializer_class = PurchaseListManualSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('approved', 'medicine', 'created')
    permission_classes = [D7896DjangoModelPermissions]
