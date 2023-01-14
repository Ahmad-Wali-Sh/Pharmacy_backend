from django.shortcuts import render
from rest_framework import viewsets

from medician.models import Pharm_Group, Medician, Kind, Country
from .serializers import PharmGroupSeralizer, MedicianSeralizer, KindSerializer, CountrySerializer

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

# Create your views here.
