from django.shortcuts import render
from rest_framework import viewsets

from medician.models import Pharm_Group, Medician, Kind, Country, Unit
from prescriptions.models import Prescription

from .serializers import PharmGroupSeralizer, MedicianSeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer, UnitSeralizer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class MedicianView(viewsets.ModelViewSet):
    queryset = Medician.objects.all()
    serializer_class = MedicianSeralizer
    # pagination_class = StandardResultsSetPagination

    # def get_queryset(self):

    #     queryset = self.queryset

    #     med = self.request.query_params.get("med")

    #     if med:
    #         queryset.filter(brand_name=med)
    #     return queryset

class KindView(viewsets.ModelViewSet):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer

class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class PharmGroupView(viewsets.ModelViewSet):
    queryset = Pharm_Group.objects.all()
    serializer_class = PharmGroupSeralizer

class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class UnitView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSeralizer

# Create your views here.
