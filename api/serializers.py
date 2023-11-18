from rest_framework import serializers
from django.core import serializers as core_serializers
import io
from django.db.models import F

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, \
    Outrance, OutranceThrough, City, Market, Revenue, RevenueTrough, EntranceImage, User, MedicineWith, BigCompany, MedicineConflict, PurchaseList, PurchaseListManual

from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')
        read_only_fields = ('username', 'first_name')
        read_and_write_fields = ('id',)


class PharmGroupSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = PharmGroup
        fields = '__all__'


class RevenueSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_employee_name(self, obj):
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
    patient_name = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        if (obj.prescription.name):
            return str(obj.prescription.name.id) + "." + obj.prescription.name.name

    def get_prescription_user(self, obj):
        return obj.prescription.user.username

    def get_discount(self, obj):
        return obj.prescription.discount_percent

    def get_zakat(self, obj):
        return obj.prescription.zakat

    def get_khairat(self, obj):
        return obj.prescription.khairat

    def get_rounded(self, obj):
        return obj.prescription.rounded_number

    def get_username(self, obj):
        return obj.user.username

    def get_prescription_number(self, obj):
        return obj.prescription.prescription_number

    def get_grand_total(self, obj):
        return obj.prescription.grand_total

    def get_department(self, obj):
        return obj.prescription.department.name

    prescription = serializers.PrimaryKeyRelatedField(
        queryset=Prescription.objects.all()
    )

    class Meta:
        model = RevenueTrough
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Market
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = City
        fields = '__all__'


class PurchaseListSerializer(serializers.ModelSerializer):
    market_1 = serializers.SerializerMethodField()
    market_2 = serializers.SerializerMethodField()
    market_3 = serializers.SerializerMethodField()
    company_1_name = serializers.SerializerMethodField()
    company_2_name = serializers.SerializerMethodField()
    company_3_name = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()

    def get_medicine_full(self, res):
        obj = res.medicine
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + obj.ml + ' ' + big_company_name + country_name + " " + weight

    def get_market_1(self, obj):
        if (obj.company_1.market):
            return obj.company_1.market.name
        else:
            return ""

    def get_market_2(self, obj):
        if (obj.company_2.market):
            return obj.company_2.market.name
        else:
            return ""

    def get_market_3(self, obj):
        if (obj.company_3.market):
            return obj.company_3.market.name
        else:
            return ""

    def get_company_1_name(self, obj):
        if (obj.company_1):
            return obj.company_1.name
        return ""

    def get_company_2_name(self, obj):
        if (obj.company_2):
            return obj.company_2.name
        return ""

    def get_company_3_name(self, obj):
        if (obj.company_3):
            return obj.company_3.name
        return ""

    class Meta:
        model = PurchaseList
        fields = ['id', 'medicine_full', 'need_quautity', 'company_1_name', 'market_1', 'price_1', 'bonus_1', 'date_1', 'company_2_name',
                  'market_2', 'price_2', 'bonus_2', 'date_2', 'company_3_name', 'market_3', 'price_3', 'bonus_3', 'date_3', 'arrival_quantity', 'shortaged']


class PurchaseListQuerySerializer(serializers.ModelSerializer):
    medicine_full = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    medicine_unsubmited = serializers.SerializerMethodField()

    def get_medicine_unsubmited(self, obj):
        return obj.unsubmited_existence

    def get_quantity(self, obj):
        return obj.maximum_existence - obj.existence

    def get_details(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.id).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[:3]
        return queryset

    def get_medicine_full(self, res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    class Meta:
        model = Medician
        fields = ['id', 'medicine_full', 'quantity',
                  'details', 'medicine_unsubmited', 'shorted']


class KindSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Kind
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Country
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        if (obj.name):
            return str(obj.name.id) + "." + obj.name.name

    def get_doctor_name(self, obj):
        if (obj.doctor):
            return str(obj.doctor.id) + "." + obj.doctor.name

    def get_username(self, obj):
        return obj.user.username

    def get_department_name(self, obj):
        return obj.department.name

    class Meta:
        model = Prescription
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
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
    medicine_full = serializers.SerializerMethodField()
    kind_image = serializers.SerializerMethodField()
    country_image = serializers.SerializerMethodField()
    pharm_group_image = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=True)

    def get_department_name(self, obj):
        if (obj.department):
            return obj.department.name
        else:
            ""

    def get_kind_image(self, obj):
        if (obj.kind and obj.kind.image):
            return 'http://127.0.0.1:8000/' + str(obj.kind.image)

    def get_country_image(self, obj):
        if (obj.country and obj.country.image):
            return 'http://127.0.0.1:8000/' + str(obj.country.image)
        else:
            return ""

    def get_pharm_group_image(self, obj):
        if (obj.pharm_group and obj.pharm_group.image):
            return 'http://127.0.0.1:8000/' + str(obj.pharm_group.image)
        else:
            return ""

    def get_medicine_full(self, res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    def get_kind_name(self, obj):
        if obj.kind:
            return obj.kind.name_english
        else:
            return ""

    def get_country_name(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return ""

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Medician
        fields = '__all__'
        extra_kwargs = {'medicines': {'required': False}}


class MeidicainExcelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
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

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Unit
        fields = '__all__'


class PharmCompanySeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    market_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_market_name(self, obj):
        if (obj.market):
            return obj.market.name
        else:
            return ''

    def get_city_name(self, obj):
        if (obj.city):
            return obj.city.name
        else:
            return ''

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = PharmCompany
        fields = '__all__'


class MedicineWithSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineWith
        fields = '__all__'


class MedicineConflictSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineConflict
        fields = '__all__'


class EntranceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()
    entrance_image = serializers.SerializerMethodField()

    def get_entrance_image(self, obj):
        entrance_image_obj = EntranceImage.objects.filter(entrance=obj.id)
        json_entrance_image = EntranceImageSeriazlier(
            entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_username(self, obj):
        return obj.user.username

    def get_currency_name(self, obj):
        return obj.currency.name

    class Meta:
        model = Entrance
        fields = '__all__'


class EntranceImageSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = EntranceImage
        fields = '__all__'


class EntranceThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_min_expire = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    def get_medicine_min_expire(self, obj):
        return obj.medician.min_expire_date

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = EntranceThrough
        fields = '__all__'


class EntranceThroughExpiresSerializer(serializers.ModelSerializer):
    medician = MedicianSeralizer()

    class Meta:
        model = EntranceThrough
        fields = ('medician',)


class StoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Store
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Currency
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class FinalRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = FinalRegister
        fields = '__all__'


class DoctorNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = DoctorName
        fields = '__all__'


class PatientNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = PatientName
        fields = '__all__'


class PurchaseListManualSerializer (serializers.ModelSerializer):
    medicine_full = serializers.SerializerMethodField()
    existence = serializers.SerializerMethodField()
    details_1 = serializers.SerializerMethodField()
    details_2 = serializers.SerializerMethodField()
    details_3 = serializers.SerializerMethodField()

    def get_details_1(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[0:1]
        data = list(queryset)
        return data

    def get_details_2(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[1:2]
        data = list(queryset)
        return data

    def get_details_3(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[2:3]
        data = list(queryset)
        return data

    def get_existence(self, obj):
        return obj.medicine.existence

    def get_medicine_full(self, res):
        obj = res.medicine
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ""
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    class Meta:
        model = PurchaseListManual
        fields = '__all__'


class PrescriptionThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_cautions = serializers.SerializerMethodField()
    medicine_usage = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ""
        ml = ''
        weight = ''
        if (obj.kind):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + generics + big_company_name + country_name + " " + weight

    def get_medicine_cautions(self, obj):
        if (obj.medician.cautions):
            return obj.medician.cautions
        else:
            return ""

    def get_medicine_usage(self, obj):
        if (obj.medician.usages):
            return obj.medician.usages
        else:
            return ""

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = PrescriptionThrough
        fields = '__all__'


class OutranceSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Outrance
        fields = '__all__'


class OutranceThroughSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = OutranceThrough
        fields = '__all__'


class TrazSerializer (serializers.Serializer):
    entrances = EntranceThroughSerializer(many=True)
    prescriptions = PrescriptionThroughSerializer(many=True)
