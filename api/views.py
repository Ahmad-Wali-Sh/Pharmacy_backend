from django.shortcuts import render
from rest_framework import viewsets

from medician.models import Pharm_Group, Medician, Kind, Country
from prescriptions.models import Prescription

from .serializers import PharmGroupSeralizer, MedicianSeralizer, KindSerializer, CountrySerializer, PrescriptionSerializer

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
    queryset = Pharm_Group.objects.all()
    serializer_class = PharmGroupSeralizer

class PrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

# Create your views here.
