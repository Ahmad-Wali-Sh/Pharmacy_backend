from rest_framework import serializers

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough
                        


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
        fields = '__all__'


class UnitSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class PharmCompanySeralizer(serializers.ModelSerializer):
    class Meta:
        model = PharmCompany
        fields = '__all__'


class EntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrance
        fields = '__all__'


class EntranceThroughSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceThrough
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        
class FinalRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalRegister
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DoctorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorName
        fields = '__all__'

        
class PatientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientName
        fields = '__all__'

        

class PrescriptionThroughSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionThrough
        fields = '__all__'