from rest_framework import serializers

from prescription.models import Prescription, Pharm_Group, Kind, Country

class PrescriptionSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class PharmGroupSeralizer(serializers.ModelSerializer):
    class Meta: 
        model = Pharm_Group
        fields = '__all__'

class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'