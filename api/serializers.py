from rest_framework import serializers

<<<<<<< HEAD
from core.models import Medician, PharmGroup, Kind, Country, Unit, Prescription, PharmCompany, Entrance
=======
from core.models import Medician, PharmGroup, Kind, Country, Unit, Prescription, PharmCompany, Entrance, EntranceThrough
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2


class PharmGroupSeralizer(serializers.ModelSerializer):
    class Meta:
        model = PharmGroup
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
        fields = ('id', 'brand_name', 'generic_name', 'no_pocket', 'pharm_group', 'kind', 'ml', 'unit', 'weight',
                  'location', 'country', 'company', 'barcode', 'price', 'minmum_existence', 'maximum_existence',
                  'dividing_rules', 'cautions', 'usages', 'description', 'image')


class UnitSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class PharmCompanySeralizer(serializers.ModelSerializer):
    class Meta:
        model = PharmCompany
        fields = '__all__'

<<<<<<< HEAD

class EntranceSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Entrance
        fields = '__all__'
=======
class EntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrance
        fields = '__all__'

class EntranceThroughSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceThrough
        fields = '__all__'
>>>>>>> 0ff627eda673f2af0dc730279b1ca73427865ef2
