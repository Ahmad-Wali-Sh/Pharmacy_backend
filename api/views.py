from django.shortcuts import render
from rest_framework import generics

from prescription.models import Pharm_Group, Prescription, Kind, Country
from .serializers import PharmGroupSeralizer, PrescriptionSeralizer, KindSerializer, CountrySerializer

class PrescriptionView(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSeralizer

class KindView(generics.ListAPIView):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer

class CountryView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class PharmGroupView(generics.ListAPIView):
    queryset = Pharm_Group.objects.all()
    serializer_class = PharmGroupSeralizer

# Create your views here.
