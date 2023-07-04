from rest_framework import serializers

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, \
        Outrance, OutranceThrough, City, Market, Revenue, RevenueTrough, User
                        
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)
        read_only_fields = ('username',)
        read_and_write_fields = ('id',)

class PharmGroupSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = PharmGroup
        fields = '__all__'

class RevenueSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Revenue
        fields = '__all__'




class MarketSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Market
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = City
        fields = '__all__'


class KindSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Kind
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Country
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Prescription
        fields = '__all__'

class RevenueTrhoughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    prescription = serializers.PrimaryKeyRelatedField(
        queryset= Prescription.objects.all()
    )
    class Meta:
        model = RevenueTrough
        fields = '__all__'     


class MedicianSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Medician
        fields = '__all__'

class MeidicainExcelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    
    kind = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name_english',
    )
    pharm_group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name_english'
    )
    country = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Medician
        fields = '__all__'


class UnitSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = Unit
        fields = '__all__'


class PharmCompanySeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = PharmCompany
        fields = '__all__'


class EntranceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    # factor_date = JDateTimeField()
    class Meta:
        model = Entrance
        fields = '__all__'


class EntranceThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = EntranceThrough
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = Store
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = Currency
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        
class FinalRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = FinalRegister
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = Department
        fields = '__all__'




class DoctorNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = DoctorName
        fields = '__all__'

        
class PatientNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = PatientName
        fields = '__all__'

        

class PrescriptionThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = PrescriptionThrough
        fields = '__all__'


class OutranceSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Outrance
        fields = '__all__'

class OutranceThroughSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = OutranceThrough
        fields = '__all__'

class TrazSerializer (serializers.Serializer):
    entrances = EntranceThroughSerializer(many=True)
    prescriptions = PrescriptionThroughSerializer(many=True)
