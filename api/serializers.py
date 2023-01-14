from rest_framework import serializers

from medician.models import Medician, Pharm_Group, Kind, Country

class MedicianSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Medician
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