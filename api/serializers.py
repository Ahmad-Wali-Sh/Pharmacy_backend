from rest_framework import serializers

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, \
        Outrance, OutranceThrough, City, Market, Revenue, RevenueTrough, User, MedicineWith, BigCompany
                        
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
    employee_name = serializers.SerializerMethodField()


    def get_username (self, obj):
        return obj.user.username
    
    def get_employee_name (self, obj):
        return obj.employee.username

    class Meta:
        model = Revenue
        fields = '__all__'

class RevenueTrhoughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    prescription_user = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    zakat = serializers.SerializerMethodField()
    khairat = serializers.SerializerMethodField()
    rounded = serializers.SerializerMethodField()
    

    def get_prescription_user (self,obj):
        return obj.prescription.user.username

    def get_discount (self,obj):
        return obj.prescription.discount_percent
    def get_zakat (self,obj):
        return obj.prescription.zakat
    def get_khairat (self,obj):
        return obj.prescription.khairat
    def get_rounded (self,obj):
        return obj.prescription.rounded_number

    def get_username (self, obj):
        return obj.user.username

    def get_prescription_number (self, obj):
        return obj.prescription.prescription_number

    def get_grand_total (self, obj):
        return obj.prescription.grand_total

    def get_department (self, obj):
        return obj.prescription.department.name

    prescription = serializers.PrimaryKeyRelatedField(
        queryset= Prescription.objects.all()
    )
    class Meta:
        model = RevenueTrough
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
    department_name = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username

    def get_department_name (self, obj):
        return obj.department.name

    class Meta:
        model = Prescription
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    class Meta:
        model = Department
        fields = '__all__'

class BigCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = BigCompany
        fields = '__all__'



class MedicianSeralizer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_kind_name (self, obj):
        if obj.kind:
            return obj.kind.name_english
        else:
            return ""
    
    def get_country_name (self, obj):
        if obj.country:
            return obj.country.name
        else:
            return ""

    def get_username (self, obj):
        return obj.user.username

    class Meta:
        model = Medician
        fields = '__all__'
        extra_kwargs = {'medicines': {'required': False}}

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

class MedicineWithSerializer(serializers.ModelSerializer):

    class Meta: 
        model = MedicineWith
        fields = '__all__'


class EntranceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()

    def get_username (self, obj):
        return obj.user.username
    
    
    def get_currency_name (self, obj):
        return obj.currency.name

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
