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
    PrescriptionExcelSerializer,
    PaymentMethodSerializer,
    StockSerializer,
    FinalRegisterSerializer,
    DepartmentSerializer,
    DoctorNameSerializer,
    PrescriptionImageSerializer,
    PatientNameSerializer,
    PrescriptionThroughSerializer,
    MeidicainExcelSerializer,
    TrazSerializer,
    CitySerializer,
    DepartmentReturnSerializer,
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
    PrescriptionReturnSerializer,
    PrescriptionThroughReturnSerializer,
    PrescriptionReturnImageSerializer,
    PurchaseListManualSerializer,
    EntranceImageSeriazlier,
    MedicianOrderSerializer,
    RevenueRecordSerializer,
    JournalCategorySerializer,
    JournalEntrySerializer,
    SalaryEntrySerializer,
    EntranceExcelSerializer,
    UniqueMedicineSerializer,
    GlobalSettingsSerializer
)
from rest_framework_csv.renderers import CSVRenderer
from django.db.models import Subquery, OuterRef, Sum
from datetime import datetime, timedelta
from rest_framework import status
from auditlog.registry import auditlog
from django.utils.timezone import now
import jdatetime
from rest_framework.renderers import JSONRenderer

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
    DepartmentReturn,
    PrescriptionReturn,
    PrescriptionReturnThrough,
    PrescriptionReturnImage,
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
    JournalCategory,
    JournalEntry,
    SalaryEntry,
    GlobalSettings
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
from rest_framework_xml.renderers import XMLRenderer
from decimal import Decimal
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class CustomXMLRendererPrescription(XMLRenderer):
    item_tag_name = "Prescription"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            # This assumes the response structure has 'results' as the main list
            data = data.get("results", data)

        if isinstance(data, list):
            for item in data:
                self.rename_fields(item)

        return super(CustomXMLRendererPrescription, self).render(
            data, accepted_media_type, renderer_context
        )

    def rename_fields(self, item):
        # Define your custom header mappings
        field_mapping = {
            "id": "ID",
            "prescription_number": "Prescription_Number",
            "patient_name": "Patient_Name",
            "doctor_name": "Doctor_Name",
            "department_name": "Department_Name",
            "username": "Created_By",
            "order_user_name": "Ordered_By",
            "discount_money": "Discount_Money",
            "discount_percent": "Discount_Percent",
            "discount_value": "Discount_Value",
            "over_money": "Over_Money",
            "over_percent": "Over_Percent",
            "khairat": "Khairat",
            "zakat": "Zakat",
            "rounded_number": "Rounded_Number",
            "purchased_value": "Purchased_Value",
            "purchase_payment_date": "Purchase_Payment_Date",
            "revenue": "Revenue",
            "refund": "To_Purchase",
            "timestamp": "Timestamp",
            "sold": "Sold",
            "quantity": "Medicine_Count",
            "created": "Created",
        }

        for old_field, new_field in field_mapping.items():
            if old_field in item:
                item[new_field] = item.pop(old_field)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    user = request.user
    permissions = list(user.get_all_permissions())
    additional_permissions = user.additional_permissions.all()
    additional_permissions_list = [str(p) for p in additional_permissions]
    all_permissions = permissions + additional_permissions_list
    return JsonResponse({"permissions": all_permissions})


class TerminateTokenView(APIView):
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in authentication
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                # Try to retrieve the token associated with the user
                token = Token.objects.get(user=user)
                token.delete()  # Delete the token if it exists
                return Response({'detail': 'Token successfully deleted.'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                # Handle the case where the token does not exist for the user
                return Response({'detail': 'No active token found for this user.'}, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return a 401 unauthorized response
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                token = Token.objects.get(user=user)
                token.delete()
            except Token.DoesNotExist:
                pass

            new_token, created = Token.objects.get_or_create(user=user)

            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


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
    existence_lower_than_minimum_quantity = django_filters.BooleanFilter(
        method="filter_existence_lower_than_minimum_quantity"
    )

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
            return (
                queryset.filter(minmum_existence__isnull=False)
                .filter(minmum_existence__gt=0)
                .filter(active=True)
                .filter(existence__lt=F("minmum_existence"))
            )
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
        if self.action in ["list", "retrieve"]:
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
    ordering_fields = [
        "-id",
    ]
    
class StockFilter(django_filters.FilterSet):
    generic_name = django_filters.CharFilter(
        lookup_expr="icontains"
    )
    brand_name = django_filters.CharFilter(lookup_expr="istartswith")
    class Meta:
        model = Medician
        fields = [
            "brand_name",
            "generic_name",
            "company",
            "pharm_group",
            "kind",
            "country",
            "big_company"
        ]

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StockFilter
    ordering_fields = ["total_sell", "total_purchase"]
    pagination_class = StandardResultsSetPagination
    
    def get_date_range(self, shortcut):
        today = jdatetime.date.today()

        start_date = None
        end_date = None

        if shortcut == "today":
            # Start of today
            start_date = today
            # End of today (to include the entire day)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "this_week":
            start_date = today - jdatetime.timedelta(days=today.weekday())
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_week":
            start_date = today - jdatetime.timedelta(days=today.weekday() + 7)
            end_date = start_date + jdatetime.timedelta(days=6)

        elif shortcut == "this_month":
            start_date = today.replace(day=1)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_six_months":
            start_date = today - jdatetime.timedelta(days=6 * 30)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "this_year":
            start_date = today.replace(month=1, day=1)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_year":
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = start_date.replace(month=12, day=29) + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        return start_date.togregorian(), end_date.togregorian()
    
    def get_queryset (self):
        shortcut = self.request.query_params.get('shortcut')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if shortcut: 
            start_date, end_date = self.get_date_range(shortcut)
            
        prescription_filter = {}
        entrance_filter = {}
        return_filter = {}
        
        if start_date and end_date:
            prescription_filter = {"timestamp__range": [start_date, end_date]}
            entrance_filter = {"timestamp__range": [start_date, end_date]}
            return_filter = {"timestamp__range": [start_date, end_date]}
        queryset = (
            Medician.objects.filter(active=True)
            .annotate(
                total_sell=Subquery(
                    PrescriptionThrough.objects.filter(
                        medician=OuterRef('pk'), **prescription_filter
                    )
                    .values('medician')
                    .annotate(total_sell=Sum('quantity'))
                    .values('total_sell'),
                ),
                total_purchase=Subquery(
                    EntranceThrough.objects.filter(
                        medician=OuterRef('pk'), **entrance_filter
                    )
                    .values('medician')
                    .annotate(total_purchase=Sum('register_quantity'))
                    .values('total_purchase'),
                ),
                returned_quantity=Subquery(
                    PrescriptionReturnThrough.objects.filter(
                        medician=OuterRef('pk'), **return_filter
                    )
                    .values('medician')
                    .annotate(returned_quantity=Sum('quantity'))
                    .values('returned_quantity'),
                )
            )
        )
        return queryset

class StockExcelSort(CSVRenderer):
    header = [
            'id', 
            'medicine_full', 
            'brand_name', 
            'kind_name_english', 
            'kind_name_persian', 
            'ml', 
            'pharm_group_name_persian', 
            'pharm_group_name_english', 
            'country_name', 
            'big_company_name', 
            'no_box', 
            'no_pocket', 
            'existence', 
            'purchased_price', 
            'price', 
            'total_purchase', 
            'total_sell',
            'sold_quantity',
            'returned_quantity',
            'purchased_quantity'
        ]

class StockExcelView(viewsets.ModelViewSet):
    renderer_classes = (StockExcelSort,)
    serializer_class = StockSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StockFilter
    ordering_fields = ["total_sell", "total_purchase"]
    
    def get_date_range(self, shortcut):
        today = jdatetime.date.today()

        start_date = None
        end_date = None

        if shortcut == "today":
            # Start of today
            start_date = today
            # End of today (to include the entire day)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "this_week":
            start_date = today - jdatetime.timedelta(days=today.weekday())
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_week":
            start_date = today - jdatetime.timedelta(days=today.weekday() + 7)
            end_date = start_date + jdatetime.timedelta(days=6)

        elif shortcut == "this_month":
            start_date = today.replace(day=1)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_six_months":
            start_date = today - jdatetime.timedelta(days=6 * 30)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "this_year":
            start_date = today.replace(month=1, day=1)
            end_date = today + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        elif shortcut == "last_year":
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = start_date.replace(month=12, day=29) + jdatetime.timedelta(days=1) - jdatetime.timedelta(seconds=1)

        return start_date.togregorian(), end_date.togregorian()
    
    def get_queryset (self):
        shortcut = self.request.query_params.get('shortcut')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if shortcut: 
            start_date, end_date = self.get_date_range(shortcut)
            
        prescription_filter = {}
        entrance_filter = {}
        return_filter = {}
        
        if start_date and end_date:
            prescription_filter = {"timestamp__range": [start_date, end_date]}
            entrance_filter = {"timestamp__range": [start_date, end_date]}
            return_filter = {"timestamp__range": [start_date, end_date]}
        queryset = (
            Medician.objects.filter(active=True)
            .annotate(
                total_sell=Subquery(
                    PrescriptionThrough.objects.filter(
                        medician=OuterRef('pk'), **prescription_filter
                    )
                    .values('medician')
                    .annotate(total_sell=Sum('quantity'))
                    .values('total_sell'),
                ),
                total_purchase=Subquery(
                    EntranceThrough.objects.filter(
                        medician=OuterRef('pk'), **entrance_filter
                    )
                    .values('medician')
                    .annotate(total_purchase=Sum('register_quantity'))
                    .values('total_purchase'),
                ),
                returned_quantity=Subquery(
                    PrescriptionReturnThrough.objects.filter(
                        medician=OuterRef('pk'), **return_filter
                    )
                    .values('medician')
                    .annotate(returned_quantity=Sum('quantity'))
                    .values('returned_quantity'),
                )
            )
        )
        return queryset


class MedicianMinimuFilter(django_filters.FilterSet):
    existence_lower_than_minimum_quantity = django_filters.BooleanFilter(
        method="filter_existence_lower_than_minimum_quantity"
    )

    class Meta:
        model = Medician
        fields = []

    def filter_existence_lower_than_minimum_quantity(self, queryset, name, value):
        if value:
            return (
                queryset.filter(minmum_existence__isnull=False)
                .filter(minmum_existence__gt=0)
                .filter(active=True)
                .filter(existence__lt=F("minmum_existence"))
            )
        return queryset

class MedicianMinimumSorted(CSVRenderer):
    header = [
        'medicine_id',
        'medicine_full',
        'kind_persian',
        'kind_english',
        'pharm_group_persian',
        'pharm_group_english',
        'existence',
        'minimum',
        'maximum',
        'need',
        'sold_quantity',
        'purchased_quantity',
        'returned_quantity'
      ]

class MedicianMinimumViewSet(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicineMinimumSerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MedicianMinimuFilter
    ordering_fields = [
        "-id",
    ]
    renderer_classes = [JSONRenderer, MedicianMinimumSorted]


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


class PrescriptionReturnThroughView(viewsets.ModelViewSet):
    queryset = PrescriptionReturnThrough.objects.all().order_by("id")
    serializer_class = PrescriptionThroughReturnSerializer
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


class DepartmentReturnView(viewsets.ModelViewSet):
    queryset = DepartmentReturn.objects.all().order_by("id")
    serializer_class = DepartmentReturnSerializer
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

    has_prescriptionthrough = django_filters.BooleanFilter(
        method="filter_has_prescriptionthrough"
    )

    purchased = django_filters.BooleanFilter(method="filter_purchased")

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
            "purchased_value",
            "purchased",
            "discount_money",
            "zakat",
            "khairat",
            "refund",
            "prescription_number",
            "sold",
            "barcode_str",
            "revenue",
            "grand_not_equal",
        ]

    def filter_has_prescriptionthrough(self, queryset, name, value):
        if value:
            return queryset.filter(prescriptionthrough__isnull=False).distinct()
        else:
            return queryset.filter(prescriptionthrough__isnull=True).distinct()

    def filter_purchased(self, queryset, name, value):
        if value:
            return queryset.filter(purchased_value__gt=0)
        return queryset


class PrescriptionReturnFilterView(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter()
    refund_not_equal = django_filters.NumberFilter(
        field_name="refund", lookup_expr="exact", exclude=True
    )  # New field for refund not equal
    grand_not_equal = django_filters.NumberFilter(
        field_name="grand_total", lookup_expr="exact", exclude=True
    )  # New field for refund not equal

    has_prescriptionthrough = django_filters.BooleanFilter(
        method="filter_has_prescriptionthrough"
    )

    purchased = django_filters.BooleanFilter(method="filter_purchased")

    class Meta:
        model = PrescriptionReturn
        fields = [
            "prescription_number",
            "department",
            "created",
            "refund_not_equal",
            "name",
            "doctor",
            "order_user",
            "grand_total",
            "purchased_value",
            "purchased",
            "discount_money",
            "zakat",
            "khairat",
            "refund",
            "prescription_number",
            "sold",
            "barcode_str",
            "revenue",
            "grand_not_equal",
        ]

    def filter_has_prescriptionthrough(self, queryset, name, value):
        if value:
            return queryset.filter(prescriptionthrough__isnull=False).distinct()
        else:
            return queryset.filter(prescriptionthrough__isnull=True).distinct()

    def filter_purchased(self, queryset, name, value):
        if value:
            return queryset.filter(purchased_value__gt=0)
        return queryset


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

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        try:
            prescription = self.get_object()

            new_prescription = Prescription.objects.create(
                department=prescription.department,
                name=prescription.name,
                doctor=prescription.doctor,
                discount_money=prescription.discount_money,
                discount_percent=prescription.discount_percent,
                over_money=prescription.over_money,
                over_percent=prescription.over_percent,
                zakat=prescription.zakat,
                khairat=prescription.khairat,
                image=prescription.image,
                user=request.user
            )

            prescription_throughs = PrescriptionThrough.objects.filter(
                prescription=pk
            ).order_by("id")
            for through in prescription_throughs:
                medician = Medician.objects.get(pk=through.medician.pk)
                through.pk = None
                through.prescription = new_prescription
                through.each_price = medician.price
                through.total_price = float(medician.price) * float(through.quantity)
                through.user = request.user
                through.save()

            serializer = self.get_serializer(new_prescription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Prescription.DoesNotExist:
            return Response(
                {"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionReturnView(viewsets.ModelViewSet):
    queryset = PrescriptionReturn.objects.all().order_by("id")
    serializer_class = PrescriptionReturnSerializer
    filterset_class = PrescriptionReturnFilterView
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [D7896DjangoModelPermissions]
    ordering_fields = ["id", "created", "purchase_payment_date"]


class PrescriptionPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = "page_size"
    max_page_size = 60

    def calculate_discount_and_grand_total(self, prescriptions):
        grand_total_sum = 0
        discount_value_sum = 0

        for prescription in prescriptions:
            # Validate the presence of 'id' in each prescription
            if "id" not in prescription:
                raise ValueError("Prescription ID is missing.")

            try:
                # Calculate grand total for each prescription based on PrescriptionThrough
                grand_total = (
                    PrescriptionThrough.objects.filter(
                        prescription_id=prescription["id"]
                    ).aggregate(grand_total=Sum("total_price"))["grand_total"]
                    or 0
                )
            except Exception as e:
                # Handle any exceptions that occur during the query
                raise ValueError(
                    f"Error calculating grand total for prescription ID {prescription['id']}: {str(e)}"
                )

            purchased_value = prescription.get("purchased_value", 0)
            discount_percent = prescription.get("discount_percent", 0)
            discount_money = prescription.get("discount_money", 0)

            # Calculate discount value based on the discount type
            if discount_percent == 0:
                discount_value = discount_money
            elif discount_percent > 100:
                discount_value = purchased_value + discount_money
            elif discount_percent == 100:
                discount_value = grand_total
            else:
                discount_percent_value = grand_total * (discount_percent / 100)
                discount_value = discount_money + discount_percent_value

            grand_total_sum += grand_total
            discount_value_sum += discount_value

        return grand_total_sum, discount_value_sum

    def get_paginated_response(self, data):
        queryset = self.page.paginator.object_list
        prescriptions = list(
            queryset.values(
                "purchased_value",
                "discount_percent",
                "discount_money",
                "grand_total",
                "id",
            )
        )

        try:
            grand_total_sum, discount_value_sum = (
                self.calculate_discount_and_grand_total(prescriptions)
            )
        except ValueError as e:
            # Handle any errors during the calculation
            return Response({"error": str(e)}, status=400)

        # Aggregate other totals from the queryset
        total_grand_total = (
            queryset.aggregate(Sum("purchased_value"))["purchased_value__sum"] or 0
        )
        total_zakat = queryset.aggregate(Sum("zakat"))["zakat__sum"] or 0
        total_khairat = queryset.aggregate(Sum("khairat"))["khairat__sum"] or 0
        total_rounded_number = (
            queryset.aggregate(Sum("rounded_number"))["rounded_number__sum"] or 0
        )
        total_over_money = queryset.aggregate(Sum("over_money"))["over_money__sum"] or 0
        total_discount_money = (
            queryset.aggregate(Sum("discount_money"))["discount_money__sum"] or 0
        )
        total_discount_percent = (
            queryset.aggregate(Sum("discount_percent"))["discount_percent__sum"] or 0
        )
        total_to_sell = queryset.aggregate(Sum("refund"))["refund__sum"] or 0

        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "current_page": self.page.number,
                "total_grand_total": grand_total_sum,  # Use calculated grand_total_sum
                "total_zakat": total_zakat or 0,
                "total_over_money": total_over_money or 0,
                "total_khairat": total_khairat or 0,
                "total_discount_money": total_discount_money or 0,
                "total_discount_percent": total_discount_percent or 0,
                "total_discount_value": discount_value_sum or 0,
                "total_rounded_number": total_rounded_number or 0,
                "total_pages": self.page.paginator.num_pages,
                "total_to_sell": total_to_sell or 0,
                "results": data,
            }
        )


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


class PrescriptionReturnPaginatedView(viewsets.ModelViewSet):
    queryset = PrescriptionReturn.objects.all().order_by("id")
    serializer_class = PrescriptionReturnSerializer
    filterset_class = PrescriptionReturnFilterView
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [D7896DjangoModelPermissions]
    ordering_fields = ["id", "created", "purchase_payment_date"]
    pagination_class = StandardResultsSetPagination


class LastPrescriptionReturnView(viewsets.ModelViewSet):
    queryset = PrescriptionReturn.objects.all().order_by("-id")[:1]
    serializer_class = PrescriptionReturnSerializer
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

WHOLESALE_CHOICE = (("WHOLESALE", "WHOLESALE"), ("SINGULAR", "SINGULAR"))
class EntranceFilterView(django_filters.FilterSet):
    factor_date = django_filters.DateFromToRangeFilter()
    wholesale = django_filters.ChoiceFilter(choices=WHOLESALE_CHOICE)

    class Meta:
        model = Entrance
        fields = [
            "id",
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
            'user'
        ]
class EntranceSortedRenderer(CSVRenderer):
    header = [
      "id",
      "factor_number",
      "final_register_name",
      "company_name",
      "store_name",
      "payment_method_name",
      "currency_name",
      "currency_rate",
      "entrance_through_count",
      "total_before_discount",
      "discount_value",
      "bonus_quantity",
      "total_sell",
      "total_interest",
      "total_interest_percent",
      "grand_total",
      "grand_total_afg",
      "deliver_by",
      "recived_by",
      "factor_date",
      "wholesale",
      "username",
      "description",
      ]


class EntranceThroughExcelFilterView(django_filters.FilterSet):
    factor_number = django_filters.NumberFilter(field_name='entrance__factor_number')
    factor_date = django_filters.DateFromToRangeFilter(field_name='entrance__factor_date')
    total_interest = django_filters.NumberFilter(field_name='entrance__total_interest')
    company = django_filters.CharFilter(field_name='entrance__company')
    currency = django_filters.CharFilter(field_name='entrance__currency')
    deliver_by = django_filters.CharFilter(field_name='entrance__deliver_by')
    received_by = django_filters.CharFilter(field_name='entrance__recived_by')
    discount_percent = django_filters.NumberFilter(field_name='entrance__discount_percent')
    payment_method = django_filters.CharFilter(field_name='entrance__payment_method')
    wholesale = django_filters.ChoiceFilter(field_name='entrance__wholesale', choices=WHOLESALE_CHOICE)
    final_register = django_filters.CharFilter(field_name='entrance__final_register')
    store = django_filters.CharFilter(field_name='entrance__store' )
    user = django_filters.CharFilter(field_name='entrance__user')
    id = django_filters.CharFilter(field_name='entrance__id')
    
    class Meta:
        model = EntranceThrough
        fields = [
            'id',
            'medician',          
            'entrance',              
            'factor_number',         
            'factor_date',          
            'total_interest',       
            'company',             
            'currency',             
            'deliver_by',           
            'received_by',         
            'discount_percent',    
            'payment_method',             
            'wholesale',         
            'final_register',    
            'store',          
            'user'         
        ]
class EntranceTroughSortedRenderer(CSVRenderer):
    header = [
    "id",
    "username",
    "medician",
    "medicine_full",
    "medicine_existence",
    "company_name",
    "entrance",
    "entrance_department",
    "rate_name",
    "rate",
    "number_in_factor",
    "each_price_factor",
    "each_price",
    "discount_money",
    "no_box",
    "discount_percent",
    "total_purchaseـafghani",
    "total_purchaseـcurrency",
    "total_purchase_currency_before",
    "discount_value",
    "each_quantity",
    "quantity_bonus",
    "bonus_value",
    "shortage",
    "lease",
    "each_purchase_price",
    "each_sell_price",
    "each_sell_price_afg",
    "total_sell",
    "interest_percent",
    "register_quantity",
    "total_interest",
    "expire_date",
    "timestamp",
    "batch_number",
    "interest_money",
    "bonus_interest",
      ]  
    
class EntranceThroughExcelView(viewsets.ModelViewSet):
    queryset = EntranceThrough.objects.all().order_by("id")
    serializer_class = EntranceThroughSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceThroughExcelFilterView
    permission_classes = [D7896DjangoModelPermissions]
    renderer_classes = (EntranceTroughSortedRenderer,)
class EntranceExcelView (viewsets.ModelViewSet):
    queryset = Entrance.objects.all().order_by("id")
    serializer_class = EntranceExcelSerializer
    renderer_classes = (EntranceSortedRenderer,)
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EntranceFilterView

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


class PrescriptionReturnImageView(viewsets.ModelViewSet):
    queryset = PrescriptionReturnImage.objects.all().order_by("id")
    serializer_class = PrescriptionReturnImageSerializer
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
        if self.request.method in ["GET"]:
            return MedicineWithGetSerializer
        elif self.request.method in ["POST", "PATCH", "PUT", "DELETE"]:
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
        {
            "queryset": PrescriptionReturnThrough.objects.all(),
            "serializer_class": PrescriptionThroughReturnSerializer,
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

    def get_queryset(self):
        # Return the queryset for the model defined in the view
        return EntranceThrough.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        medicine = request.query_params.get("medician")

        entrance_throughs = EntranceThrough.objects.filter(medician=medicine)

        prescription_throughs = PrescriptionThrough.objects.filter(medician=medicine)

        prescription_return_throughs = PrescriptionReturnThrough.objects.filter(
            medician=medicine
        )

        entrance_through_total = (
            entrance_throughs.aggregate(total=Sum("register_quantity"))["total"] or 0
        )

        prescription_through_total = (
            prescription_throughs.aggregate(total=Sum("quantity"))["total"] or 0
        )

        prescription_return_through_total = (
            prescription_return_throughs.aggregate(total=Sum("quantity"))["total"] or 0
        )

        response_data = {
            "results": response.data,
            "entrance_through_total": entrance_through_total,
            "prescription_through_total": prescription_through_total,
            "prescription_return_through_total": prescription_return_through_total,
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
        "revenue",
        "prescription__prescription_number",
        "record_type",
        "amount",
    ]
    pagination_class = StandardResultsSetPagination
    
class PrescriptionSortedView (CSVRenderer):
    header = {
            "id": "ID",
            "prescription_number": "Prescription_Number",
            "patient_name": "Patient_Name",
            "doctor_name": "Doctor_Name",
            "department_name": "Department_Name",
            "username": "Created_By",
            "order_user_name": "Ordered_By",
            "discount_money": "Discount_Money",
            "discount_percent": "Discount_Percent",
            "discount_value": "Discount_Value",
            "over_money": "Over_Money",
            "over_percent": "Over_Percent",
            "khairat": "Khairat",
            "zakat": "Zakat",
            "rounded_number": "Rounded_Number",
            "purchased_value": "Purchased_Value",
            "purchase_payment_date": "Purchase_Payment_Date",
            "revenue": "Revenue",
            "refund": "To_Purchase",
            "timestamp": "Timestamp",
            "sold": "Sold",
            "quantity": "Medicine_Count",
            "created": "Created",
        }


class PrescriptionExcelView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("id")
    serializer_class = PrescriptionExcelSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PrescriptionFilterView
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]
    permission_classes = [D7896DjangoModelPermissions]
    renderer_classes = (PrescriptionSortedView,)


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

    @action(detail=True, methods=["get"], url_path="previous")
    def previous(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = Prescription.objects.filter(
                department=prescription.department, id__lt=prescription.id
            ).order_by("-id")

            if department_prescriptions.exists():
                previous_prescription = department_prescriptions.first()
                serializer = self.get_serializer(previous_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "No previous prescription found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Prescription.DoesNotExist:
            return Response(
                {"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"], url_path="next")
    def next(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = Prescription.objects.filter(
                department=prescription.department, id__gt=prescription.id
            ).order_by("id")

            if department_prescriptions.exists():
                next_prescription = department_prescriptions.first()
                serializer = self.get_serializer(next_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "No next prescription found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Prescription.DoesNotExist:
            return Response(
                {"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND
            )


class PrescriptionReturnViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionReturn.objects.all()
    serializer_class = PrescriptionReturnSerializer

    @action(detail=True, methods=["get"], url_path="previous")
    def previous(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = PrescriptionReturn.objects.filter(
                department=prescription.department, id__lt=prescription.id
            ).order_by("-id")

            if department_prescriptions.exists():
                previous_prescription = department_prescriptions.first()
                serializer = self.get_serializer(previous_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "No previous prescription found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except PrescriptionReturn.DoesNotExist:
            return Response(
                {"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"], url_path="next")
    def next(self, request, pk=None):
        try:
            prescription = self.get_object()
            department_prescriptions = PrescriptionReturn.objects.filter(
                department=prescription.department, id__gt=prescription.id
            ).order_by("id")

            if department_prescriptions.exists():
                next_prescription = department_prescriptions.first()
                serializer = self.get_serializer(next_prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "No next prescription found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except PrescriptionReturn.DoesNotExist:
            return Response(
                {"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND
            )


class JournalCategoryView(viewsets.ModelViewSet):
    queryset = JournalCategory.objects.all().order_by("id")
    serializer_class = JournalCategorySerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name", "info", "user"]


class JournalEntryFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFilter(field_name="timestamp", lookup_expr="date")

    class Meta:
        model = JournalEntry
        fields = [
            "related_user",
            "amount",
            "category__name",
            "description",
            "user",
            "timestamp",
        ]


class JournalEntryView(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all().order_by("id")
    serializer_class = JournalEntrySerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JournalEntryFilter


class SalaryEntryFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFilter(field_name="timestamp", lookup_expr="date")
    payment_date = django_filters.DateFromToRangeFilter(field_name="payment_date")
    checked = django_filters.BooleanFilter(field_name="checked")
    amount = django_filters.NumberFilter(field_name="amount", lookup_expr="exact")
    penalty = django_filters.NumberFilter(field_name="penalty", lookup_expr="gt")
    bonus = django_filters.NumberFilter(field_name="bonus", lookup_expr="gt")
    employee = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model: SalaryEntry
        fields = ["employee", "payment_date", "amount", "checked", "penalty", "bonus"]


class SalaryEntryViewSet(viewsets.ModelViewSet):
    queryset = SalaryEntry.objects.all().order_by("id")
    serializer_class = SalaryEntrySerializer
    permission_classes = [D7896DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SalaryEntryFilter
    pagination_class = StandardResultsSetPagination


class ExpiryMedicineFilter(django_filters.FilterSet):
    expire_in = django_filters.NumberFilter(method="filter_expire_in")

    class Meta:
        model = EntranceThrough
        fields = ["expire_in"]

    def filter_expire_in(self, queryset, name, value):
        if value is None or value <= 0:
            return queryset

        today = datetime.today()
        try:
            # Convert value to float if it's Decimal
            if isinstance(value, Decimal):
                value = float(value)

            # Calculate the date range based on the number of months until expiration
            end_date = today + timedelta(
                days=int(value * 30)
            )  # Approximate month as 30 days
            return queryset.filter(expire_date__lte=end_date)
        except (ValueError, TypeError) as e:
            # Log the error or handle it appropriately
            return queryset


class UniqueMedicineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UniqueMedicineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpiryMedicineFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return EntranceThrough.objects.distinct("medician")
   
class GlobalSettingsView(APIView):
    def get(self, request):
        """
        Get the global settings.
        """
        try:
            settings = GlobalSettings.get_settings()
            serializer = GlobalSettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GlobalSettings.DoesNotExist:
            return Response({"detail": "Settings not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        """
        Update the global settings.
        """
        try:
            settings = GlobalSettings.get_settings()
            serializer = GlobalSettingsSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except GlobalSettings.DoesNotExist:
            return Response({"detail": "Settings not found."}, status=status.HTTP_404_NOT_FOUND)