from rest_framework import permissions
from .serializers import (
    PharmGroupSeralizer,
    MedicianSeralizer,
    PharmCompanySeralizer,
    KindSerializer,
    CountrySerializer,
    PrescriptionSerializer,
    UnitSeralizer,
    StoreSerializer,
    CurrencySerializer,
    EntranceSerializer,
    EntranceThroughSerializer,
    PaymentMethodSerializer,
    FinalRegisterSerializer,
    DepartmentSerializer,
    DoctorNameSerializer,
    PrescriptionImageSerializer,
    PatientNameSerializer,
    PrescriptionThroughSerializer,
    MeidicainExcelSerializer,
    TrazSerializer,
    CitySerializer,
    MarketSerializer,
    MedicineMinimumSerializer,
    RevenueSerializer,
    UserSerializer,
    MedicineWithGetSerializer,
    MedicineWithPostSerializer,
    BigCompanySerializer,
    EntranceThroughExpiresSerializer,
    MedicineConflictSerializer,
    PurchaseListSerializer,
    PurchaseListQuerySerializer,
    MedicineBarcodeDisplaySerializer,
    MedicineBarcodeCreateUpdateSerializer,
    PurchaseListManualSerializer,
    EntranceImageSeriazlier,
    MedicianOrderSerializer,
    RevenueRecordSerializer
)
from rest_framework import status
from django.db.models import Sum

from rest_framework.pagination import PageNumberPagination
from core.models import (
    PharmGroup,
    Medician,
    Kind,
    Country,
    Unit,
    Prescription,
    PharmCompany,
    Store,
    Currency,
    Entrance,
    PrescriptionImage,
    EntranceThrough,
    PaymentMethod,
    FinalRegister,
    Department,
    DoctorName,
    PatientName,
    PrescriptionThrough,
    City,
    Market,
    Revenue,
    RevenueRecord,
    User,
    MedicineBarcode,
    EntranceImage,
    MedicineWith,
    BigCompany,
    MedicineConflict,
    PurchaseList,
    PurchaseListManual,
)
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
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    user = request.user
    permissions = list(user.get_all_permissions())
    additional_permissions = user.additional_permissions.all()
    additional_permissions_list = [str(p) for p in additional_permissions]
    all_permissions = permissions + additional_permissions_list
    return JsonResponse({"permissions": all_permissions})


class ArrayOverlapFilter(Filter):
    field_class = SimpleArrayField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "overlap")
        super().__init__(*args, **kwargs)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 50


def filter_by_ids(queryset, name, value):
    values = value.split(",")
    return queryset.filter(id__in=values)


def filter_by_generics(queryset, name, value):
    values = value.split(",")
    return queryset.filter(generic_name=values)


class CharArrayFilter(django_filters.BaseCSVFilter, django_filters.CharFilter):
    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ListFilter(Filter):
    def filter(self, qs, value):
        value_list = value.split(",")
        return super(ListFilter, self).filter(qs, Lookup(value_list, "in"))


class MedicianFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method=filter_by_ids)
    generic_name = django_filters.BaseInFilter(
        lookup_expr="contains", method=filter_by_generics
    )
    brand_name = django_filters.CharFilter(lookup_expr="istartswith")
    all = django_filters.CharFilter(method="all_filter", label="allSearch")
    ml = django_filters.CharFilter(lookup_expr="icontains")
    kind__name_english = django_filters.CharFilter(lookup_expr="icontains")
    kind__name_persian = django_filters.CharFilter(lookup_expr="icontains")
    pharm_group__name_english = django_filters.CharFilter(lookup_expr="icontains")
    pharm_group__name_persian = django_filters.CharFilter(lookup_expr="icontains")
    country__name = django_filters.CharFilter(lookup_expr="icontains")
    big_company__name = django_filters.CharFilter(lookup_expr="icontains")
    barcode__contains = CharArrayFilter(lookup_expr="contains", field_name="barcode")
    existence_lower_than_minimum_quantity = django_filters.BooleanFilter(method='filter_existence_lower_than_minimum_quantity')

    def all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(brand_name__icontains=value)
            | Q(generic_name__icontains=value)
            | Q(ml__icontains=value)
            | Q(country__name__icontains=value)
            | Q(pharm_group__name_english=value)
            | Q(pharm_group__name_persian=value)
            | Q(kind__name_english=value)
            | Q(kind__name_persian=value)
            | Q(big_company__name=value)
        )
        
    def filter_existence_lower_than_minimum_quantity(self, queryset, name, value):
        if value:
            return queryset.filter(minmum_existence__isnull=False).filter(minmum_existence__gt=0).filter(active=True).filter(existence__lt=F('minmum_existence'))
        return queryset

    class Meta:
        model = Medician
        filter_fields = {"barcode": ["exact", "icontains"]}
        fields = [
            "brand_name",
            "all",
            "generic_name",
            "no_pocket",
            "ml",
            "active",
            "location",
            "barcode__contains",
            "company",
            "price",
            "existence",
            "pharm_group",
            "kind",
            "country",
            "department",
            "pharm_group__name_english",
            "pharm_group__name_persian",
            "id",
            "ids",
            "kind__name_english",
            "country__name",
            "kind__name_persian",
            "big_company__name",
        ]
        



class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all().order_by("-id")
    serializer_class = MedicianSeralizer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["generic_name"]
    filterset_class = MedicianFilter
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination


class MedicineBarcodeView(viewsets.ModelViewSet):
    queryset = MedicineBarcode.objects.all().order_by("id")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["barcode", "medicine"]
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MedicineBarcodeDisplaySerializer
        return MedicineBarcodeCreateUpdateSerializer


class MedicianExcelView(viewsets.ModelViewSet):
    queryset = Medician.objects.all().order_by("id")
    serializer_class = MeidicainExcelSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["brand_name"]
    filterset_class = MedicianFilter
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class MedicianOrderViewSet(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianOrderSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MedicianFilter
    ordering_fields = ['-id',]
    
class MedicianMinimuFilter(django_filters.FilterSet):
    existence_lower_than_minimum_quantity = django_filters.BooleanFilter(method='filter_existence_lower_than_minimum_quantity')
    
    class Meta:
        model = Medician
        fields = []

    def filter_existence_lower_than_minimum_quantity(self, queryset, name, value):
        if value:
            return queryset.filter(minmum_existence__isnull=False).filter(minmum_existence__gt=0).filter(active=True).filter(existence__lt=F('minmum_existence'))
        return queryset
    
class MedicianMinimumViewSet(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicineMinimumSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MedicianMinimuFilter
    ordering_fields = ['-id',]


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [D7896DjangoModelPermissions]


class StoreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    phone = django_filters.CharFilter(lookup_expr="icontains")
    address = django_filters.CharFilter(lookup_expr="icontains")


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by("id")
    serializer_class = StoreSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = StoreFilter
    search_fields = [
        "name",
    ]


class FinalRegisterView(viewsets.ModelViewSet):
    queryset = FinalRegister.objects.all().order_by("id")
    serializer_class = FinalRegisterSerializer
    permission_classes = [D7896DjangoModelPermissions]


class PuchaseListView(viewsets.ModelViewSet):
    queryset = PurchaseList.objects.all().order_by("id")
    serializer_class = PurchaseListSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "company_1__market", "company_1"]
    ordering = [
        "id",
    ]


class CityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by("id")
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CityFilter
    permission_classes = [D7896DjangoModelPermissions]


class RevenueFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Revenue
        fields = ["created", "active", "employee"]


class RevenueView(viewsets.ModelViewSet):
    queryset = Revenue.objects.all().order_by("id")
    serializer_class = RevenueSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RevenueFilter
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class MarketFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")


class MarketView(viewsets.ModelViewSet):
    queryset = Market.objects.all().order_by("id")
    serializer_class = MarketSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MarketFilter


class PrescriptionThroughView(viewsets.ModelViewSet):
    queryset = PrescriptionThrough.objects.all().order_by("id")
    serializer_class = PrescriptionThroughSerializer
    filterset_fields = [
        "prescription",
    ]
    permission_classes = [D7896DjangoModelPermissions]

    @action(
        methods=["DELETE", "GET"],
        detail=False,
    )
    def delete(self, request: Request):
        delete_id = request.GET["prescription"]
        delete_prescriptions = self.queryset.filter(prescription=delete_id)
        delete_prescriptions.delete()
        return Response(self.serializer_class(delete_prescriptions, many=True).data)


class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = PatientName
        fields = ["name", "contact_number", "id", "gender", "tazkira_number"]


class PatientNameView(viewsets.ModelViewSet):
    queryset = PatientName.objects.all().order_by("id")
    serializer_class = PatientNameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PatientFilter
    permission_classes = [D7896DjangoModelPermissions]


class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = DoctorName
        fields = ["name", "contact_number", "id", "expertise"]


class DoctorNameView(viewsets.ModelViewSet):
    queryset = DoctorName.objects.all().order_by("id")
    serializer_class = DoctorNameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorFilter
    permission_classes = [D7896DjangoModelPermissions]


class BigCompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = BigCompany
        fields = [
            "name",
        ]


class BigCompanyView(viewsets.ModelViewSet):
    queryset = BigCompany.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = BigCompanySerializer
    filterset_class = BigCompanyFilter
    permission_classes = [D7896DjangoModelPermissions]
    

class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by("id")
    serializer_class = DepartmentSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        "name",
    ]
    ordering_fields = [
        "id",
    ]


class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by("id")
    serializer_class = CurrencySerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]


class PaymentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")


class PaymentMethodView(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all().order_by("id")
    serializer_class = PaymentMethodSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PaymentFilter


class KindFilter(django_filters.FilterSet):
    name_english = django_filters.CharFilter(lookup_expr="icontains")
    name_persian = django_filters.CharFilter(lookup_expr="icontains")


class KindView(viewsets.ModelViewSet):
    queryset = Kind.objects.all().order_by("id")
    serializer_class = KindSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = KindFilter
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class CountryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by("id")
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class PharmGroupFilter(django_filters.FilterSet):
    name_english = django_filters.CharFilter(lookup_expr="icontains")
    name_persian = django_filters.CharFilter(lookup_expr="icontains")


class PharmGroupView(viewsets.ModelViewSet):
    queryset = PharmGroup.objects.all().order_by("id")
    serializer_class = PharmGroupSeralizer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PharmGroupFilter
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class PrescriptionFilterView(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter()
    refund_not_equal = django_filters.NumberFilter(
        field_name="refund", lookup_expr="exact", exclude=True
    )  # New field for refund not equal
    grand_not_equal = django_filters.NumberFilter(
        field_name="grand_total", lookup_expr="exact", exclude=True
    )  # New field for refund not equal

    class Meta:
        model = Prescription
        fields = [
            "prescription_number",
            "department",
            "created",
            "refund_not_equal",
            "name",
            "doctor",
            "order_user",
            "grand_total",
            "discount_money",
            "zakat",
            "khairat",
            "refund",
            "prescription_number",
            "sold",
            "barcode_str",
            "revenue",
            "grand_not_equal"
        ]


class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("id")
    serializer_class = PrescriptionSerializer
    filterset_class = PrescriptionFilterView
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [D7896DjangoModelPermissions]
    ordering_fields = ["id", "created", "purchase_payment_date"]
    
class PrescriptionPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 60
    
    def get_paginated_response(self, data):
        
        total_grand_total = sum(item['grand_total'] for item in data if 'grand_total' in item)
        total_zakat = sum(item['zakat'] for item in data if 'zakat' in item)
        total_khairat = sum(item['khairat'] for item in data if 'khairat' in item)
        total_rounded_number = sum(item['rounded_number'] for item in data if 'rounded_number' in item)
        total_over_money = sum(item['over_money'] for item in data if 'over_money' in item)
        total_discount_money = sum(item['discount_money'] for item in data if 'discount_money' in item)
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_grand_total': total_grand_total or 0,
            'total_zakat': total_zakat or 0,
            'total_over_money': total_over_money or 0,
            'total_khairat': total_khairat or 0,
            'total_discount_money': total_discount_money or 0,
            'total_rounded_number': total_rounded_number or 0,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
    
class PrescriptionPaginatedView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("id")
    serializer_class = PrescriptionSerializer
    filterset_class = PrescriptionFilterView
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [D7896DjangoModelPermissions]
    ordering_fields = ["id", "created", "purchase_payment_date"]
    pagination_class = PrescriptionPagination


class LastPrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("-id")[:1]
    serializer_class = PrescriptionSerializer
    permission_classes = [D7896DjangoModelPermissions]


class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSeralizer
    permission_classes = [D7896DjangoModelPermissions]


class PharmCompanyView(viewsets.ModelViewSet):
    queryset = PharmCompany.objects.all().order_by("id")
    serializer_class = PharmCompanySeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    permission_classes = [D7896DjangoModelPermissions]


class EntranceFilterView(django_filters.FilterSet):
    factor_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Entrance
        fields = [
            "factor_number",
            "factor_date",
            "total_interest",
            "company",
            "currency",
            "deliver_by",
            "recived_by",
            "discount_percent",
            "payment_method",
            "medicians",
            "wholesale",
            "final_register",
            "store",
        ]


class EntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by("id")
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceFilterView
    
class EntrancePaginatedView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by("id")
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceFilterView
    pagination_class = StandardResultsSetPagination


class EntranceImageView(viewsets.ModelViewSet):
    queryset = EntranceImage.objects.all().order_by("id")
    serializer_class = EntranceImageSeriazlier
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "entrance",
    ]


class PrescriptionImageView(viewsets.ModelViewSet):
    queryset = PrescriptionImage.objects.all().order_by("id")
    serializer_class = PrescriptionImageSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "prescription",
    ]


class LastEntranceView(viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by("-id")[:1]
    serializer_class = EntranceSerializer
    permission_classes = [D7896DjangoModelPermissions]


class EntranceThroughFilterView(django_filters.FilterSet):

    class Meta:
        model = EntranceThrough
        fields = ["entrance", "medician", "medician__ml"]


class EntranceThroughView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all().order_by("id")
    serializer_class = EntranceThroughSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "medician__generic_name",
    ]
    filterset_class = EntranceThroughFilterView
    permission_classes = [D7896DjangoModelPermissions]


class EntranceThroughExpiresView(viewsets.ModelViewSet):
    serializer_class = EntranceThroughExpiresSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "medician__generic_name",
    ]
    filterset_class = EntranceThroughFilterView
    permission_classes = [D7896DjangoModelPermissions]

    def get_queryset(self):
        medicines = EntranceThrough.objects.filter(
            expire_date__lte=date.today() + relativedelta(months=6)
        )
        return medicines


class MedicineWithView(viewsets.ModelViewSet):
    queryset = MedicineWith.objects.all().order_by("id")
    permission_classes = [D7896DjangoModelPermissions]
    filterset_fields = ("medician",)
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MedicineWithGetSerializer
        elif self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return MedicineWithPostSerializer
        return MedicineWithPostSerializer


class PurchaseListQueryView(viewsets.ModelViewSet):
    queryset = Medician.objects.filter(to_buy=True) | Medician.objects.filter(
        existence__lt=F("minmum_existence")
    )
    serializer_class = PurchaseListQuerySerializer
    permission_classes = [D7896DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        "shorted",
    ]
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]


class MedicineConflictView(viewsets.ModelViewSet):
    queryset = MedicineConflict.objects.all().order_by("id")
    serializer_class = MedicineConflictSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filterset_fields = ("medicine_1",)



class MultipleModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        return True

    

class TrazView(FlatMultipleModelAPIViewSet):
    querylist = [
        {
            "queryset": EntranceThrough.objects.all(),
            "serializer_class": EntranceThroughSerializer,
        },
        {
            "queryset": PrescriptionThrough.objects.all(),
            "serializer_class": PrescriptionThroughSerializer,
        },
    ]
    model = EntranceThrough
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ("medician",)
    ordering_fields = ["id", "timestamp"]
    ordering = ["id", "timestamp"]
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        medicine = request.query_params.get('medician')

        # Filter the EntranceThrough objects based on the selected medicine and date range
        entrance_throughs = EntranceThrough.objects.filter(
            medician=medicine
        )
        
        prescription_throughs = PrescriptionThrough.objects.filter(
            medician=medicine
        )

        # Calculate the total register_quantity for the filtered EntranceThrough objects
        entrance_through_total = entrance_throughs.aggregate(
            total=Sum('register_quantity')
        )['total'] or 0
        
        prescription_through_total = prescription_throughs.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        # Calculate the totals

        # Add the totals to the response data
        response_data = {
            'results': response.data,
            'entrance_through_total': entrance_through_total,
            'prescription_through_total': prescription_through_total,
        }

        return Response(response_data)


class PurchaseListFilter(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = PurchaseListManual
        fields = ["approved", "medicine", "created"]
        
class RevenueRecordViewSet(viewsets.ModelViewSet):
    queryset = RevenueRecord.objects.all().order_by("-timestamp")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = RevenueRecordSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filterset_fields = [
        "revenue", "prescription__prescription_number", 'record_type', 'amount'
    ]
    pagination_class = PrescriptionPagination




class PurchaseListManualView(viewsets.ModelViewSet):
    queryset = PurchaseListManual.objects.all().order_by("-id")
    serializer_class = PurchaseListManualSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PurchaseListFilter
    permission_classes = [D7896DjangoModelPermissions]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    @action(detail=True, methods=['get'], url_path='previous')
    def previous(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = Prescription.objects.filter(department=prescription.department, id__lt=prescription.id).order_by('-id')

            if department_prescriptions.exists():
                previous_prescription = department_prescriptions.first()
                serializer = self.get_serializer(previous_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No previous prescription found.'}, status=status.HTTP_404_NOT_FOUND)
        except Prescription.DoesNotExist:
            return Response({'detail': 'Prescription not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['get'], url_path='next')
    def next(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = Prescription.objects.filter(department=prescription.department, id__gt=prescription.id).order_by('id')

            if department_prescriptions.exists():
                next_prescription = department_prescriptions.first()
                serializer = self.get_serializer(next_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No next prescription found.'}, status=status.HTTP_404_NOT_FOUND)
        except Prescription.DoesNotExist:
            return Response({'detail': 'Prescription not found.'}, status=status.HTTP_404_NOT_FOUND)