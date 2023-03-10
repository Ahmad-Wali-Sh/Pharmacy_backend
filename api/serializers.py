from rest_framework import serializers

from medician.models import Medician, Pharm_Group, Kind, Country, Unit
from prescriptions.models import Prescription

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

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Prescription
        fields = '__all__'

class MedicianSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Medician
        fields = ('id', 'brand_name', 'generic_name', 'no_pocket','pharm_group', 'kind', 'ml','unit', 'weight',
                 'location','country','company', 'barcode', 'price', 'minmum_existence','maximum_existence',
                 'dividing_rules','cautions', 'usages', 'description', 'image')

class UnitSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'